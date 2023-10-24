from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.fields import Base64ImageField
from core.validators import (
    validate_cart,
    validate_order,
    validate_pay_method,
    validate_send_to,
)
from products.models import (
    Category,
    Favorite,
    Order,
    OrderProductList,
    Product,
    Review,
    ShoppingCart,
    ShoppingCart_Items,
)
from users.serializers import CustomUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(required=False)
    image_2 = Base64ImageField(required=False)
    image_3 = Base64ImageField(required=False)
    image_4 = Base64ImageField(required=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'user',
            'name',
            'description',
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'video',
            'article',
            'price',
            'category',
            'is_active',
            'created',
            'modified',
        )
        read_only_fields = (
            'user',
            'article',
            'created',
            'modified',
        )


class ProductReadOnlySerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(required=False)
    image_2 = Base64ImageField(required=False)
    image_3 = Base64ImageField(required=False)
    image_4 = Base64ImageField(required=False)
    category = CategorySerializer(many=True)
    rating = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    count_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'user',
            'name',
            'description',
            'image_1',
            'image_2',
            'image_3',
            'image_4',
            'video',
            'article',
            'price',
            'rating',
            'category',
            'is_favorited',
            'is_in_shopping_cart',
            'count_in_shopping_cart',
            'is_active',
            'created',
            'modified',
        )

    @extend_schema_field({'example': [4.5, 2]})
    def get_rating(self, object):
        review = Review.objects.filter(product=object.id)
        if review.exists():
            return [
                round(review.aggregate(Avg('rating'))['rating__avg'], 1),
                review.count(),
            ]
        return [None, None]

    @extend_schema_field({'type': 'boolean', 'example': False})
    def get_is_favorited(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user,
            product=object.id,
        ).exists()

    @extend_schema_field({'type': 'boolean', 'example': False})
    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            owner=user,
            shoppingcart_items__item=object.id,
        ).exists()

    @extend_schema_field({'type': 'int', 'example': 2})
    def get_count_in_shopping_cart(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return 0
        try:
            return ShoppingCart_Items.objects.get(
                item=object.id,
                cart=ShoppingCart.objects.get(
                    owner=user,
                    shoppingcart_items__item=object.id,
                ),
            ).quantity
        except ObjectDoesNotExist:
            return 0


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    def validate(self, data):
        request = self.context['request']
        user = request.user
        product_id = self.context['view'].kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        if request.method == 'POST':
            if Review.objects.filter(product=product, user=user).exists():
                raise serializers.ValidationError(
                    {'errors': ' Вы уже оставили свой отзыв к этому товару!'},
                )
        return data

    class Meta:
        model = Review
        exclude = [
            'is_active',
        ]


class ReviewListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def get_reviews(self, obj):
        queryset = Review.objects.filter(product=obj)
        return ReviewSerializer(queryset, many=True).data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ReviewSerializer(instance, context=context).data


class ItemSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    in_favorite = serializers.SerializerMethodField()
    is_selected = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'article',
            'description',
            'image_1',
            'in_favorite',
            'category',
            'price',
            'cost',
            'quantity',
            'is_selected',
        )

    def get_quantity(self, obj):
        owner = self.context.get('request').user
        return ShoppingCart_Items.objects.get(
            item=obj,
            cart_id=owner.user_cart.id,
        ).quantity

    def get_cost(self, obj):
        return obj.price * self.get_quantity(obj)

    def get_in_favorite(self, obj):
        owner = self.context.get('request').user
        return Favorite.objects.filter(user=owner, product=obj).exists()

    def get_is_selected(self, obj):
        owner = self.context.get('request').user
        return ShoppingCart_Items.objects.get(
            item=obj,
            cart_id=owner.user_cart.id,
        ).is_selected


class ShoppingCartSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    items = ItemSerializer(read_only=True, many=True)
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'total_cost',
            'total_amount',
            'discount_amount',
            'discount',
            'items',
        )

    def get_total_cost(self, obj):
        cart = ShoppingCart_Items.objects.filter(cart=obj, is_selected=True)
        return sum([item.quantity * item.item.price for item in cart])

    def get_total_amount(self, obj):
        cart = ShoppingCart_Items.objects.filter(cart=obj, is_selected=True)
        return sum([i.quantity for i in cart])

    def get_discount_amount(self, obj):
        if obj.discount:
            total_cost = self.get_total_cost(obj)
            return int(total_cost - (total_cost / 100 * obj.discount))


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'product')

    def validate(self, data):
        request = self.context.get('request')
        product = data['product']
        if Favorite.objects.filter(
            user=request.user,
            product=product,
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Этот товар уже в избранном!'},
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ProductSerializer(instance.product, context=context).data


class OrderSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    product_list = ItemSerializer(read_only=True, many=True)
    send_to = serializers.EmailField(required=False)

    def get_total_cost(self, obj):
        user = self.context['request'].user
        cart = ShoppingCart_Items.objects.filter(cart__owner=user)
        price = sum([item.quantity * item.item.price for item in cart])
        discount = ShoppingCart.objects.get(owner=user).discount
        if discount:
            return int(price - (price * discount) / 100)
        return price

    def validate(self, data):
        send_to = validate_send_to(data.get('send_to'), self.context)
        validate_pay_method(data.get('pay_method'))
        validate_order(self.context)
        validate_cart(self.context)
        data.update(
            {
                'send_to': send_to,
            }
        )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        cart_items = ShoppingCart_Items.objects.filter(
            cart__owner=user, is_selected=True)
        order = Order.objects.create(
            user=user,
            pay_method=validated_data.get('pay_method'),
            send_to=validated_data.get('send_to'),
        )
        for item in cart_items:
            OrderProductList.objects.create(
                order=order, product=item.item, quantity=item.quantity
            )
        return order

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'pay_method',
            'total_cost',
            'send_to',
            'is_paid',
            'is_active',
            'number_order',
            'product_list',
        )
        read_only_fields = (
            'id',
            'user',
            'product_list',
            'is_paid',
            'is_active',
            'number_order',
            'created',
            'modified',
        )
