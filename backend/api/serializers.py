from django.db.models import Avg, Sum
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.fields import Base64ImageField, ListImagesField
from core.validators import (
    validate_cart,
    validate_pay_method,
    validate_send_to,
)
from products.models import (
    Category,
    Favorite,
    Image,
    ImageProduct,
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


class ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Image
        fields = ('id', 'image')


class ProductSerializer(serializers.ModelSerializer):
    images = ListImagesField(
        child=Base64ImageField(),
        required=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'user',
            'name',
            'description',
            'images',
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
            'is_active',
            'created',
            'modified',
        )

    def create(self, validated_data):
        if 'images' in self.initial_data:
            images = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        if 'images' in self.initial_data:
            for image in images:
                current_image = Image.objects.create(
                    user=product.user,
                    image=image,
                )
                ImageProduct.objects.create(
                    image=current_image,
                    product=product,
                )
        return product

    def update(self, instance, validated_data):
        method = self.context['request'].method
        if method == 'PUT':
            instance.video = None
        if 'images' in self.initial_data:
            instance.images.clear()
            images = validated_data.pop('images')
            for image in images:
                current_image = Image.objects.create(
                    user=instance.user,
                    image=image,
                )
                ImageProduct.objects.create(
                    image=current_image,
                    product=instance,
                )
        elif method == 'PUT':
            instance.images.clear()
        return super().update(instance, validated_data)

    def validate(self, data):
        if self.context['request'].user.is_seller is False:
            raise serializers.ValidationError(
                {'errors': 'Вы не являетесь продавцом!'},
            )
        return data


class ProductReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ImageSerializer(many=True)
    rating = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'user',
            'name',
            'description',
            'images',
            'video',
            'article',
            'price',
            'rating',
            'category',
            'is_favorited',
            'is_in_shopping_cart',
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
        exclude = ('created', 'modified', 'is_active')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        try:
            photo_url = request.build_absolute_uri(instance.user.photo.url)
        except ValueError:
            photo_url = None

        data['user'] = {
            'user_id': instance.user.pk,
            'username': instance.user.username,
            'photo': photo_url
        }
        return data


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
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'article',
            'description',
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
    total_quantity = serializers.SerializerMethodField()
    items = ItemSerializer(read_only=True, many=True)
    discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'total_cost',
            'total_amount',
            'total_quantity',
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

    def get_total_quantity(self, obj):
        return (
            ShoppingCart_Items.objects.filter(cart=obj)
            .aggregate(total_quantity=Sum('quantity'))
            .get('total_quantity')
        )

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


class OrderItemSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    in_favorite = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    def get_quantity(self, obj):
        user = self.context.get('request').user
        instance = self.context.get('instance')
        item = OrderProductList.objects.get(
            order__user=user,
            product=obj,
            order=instance,
        )
        return item.quantity

    def get_cost(self, obj):
        return obj.price * self.get_quantity(obj)

    def get_in_favorite(self, obj):
        user = self.context.get('request').user
        return Favorite.objects.filter(user=user, product=obj).exists()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'article',
            'description',
            'in_favorite',
            'category',
            'price',
            'cost',
            'quantity',
        )


class OrderSerializer(serializers.ModelSerializer):
    product_list = serializers.SerializerMethodField()
    send_to = serializers.EmailField(required=False)

    def get_product_list(self, obj):
        queryset = Product.objects.filter(order_with_product__order=obj)
        request = self.context.get('request')
        context = {'request': request, 'instance': obj}
        return OrderItemSerializer(queryset, many=True, context=context).data

    def validate(self, data):
        send_to = validate_send_to(data.get('send_to'), self.context)
        validate_pay_method(data.get('pay_method'))
        # validate_order(self.context)
        # Пока убрал ограничение в 1 неоплаченный заказ
        validate_cart(self.context)
        data.update(
            {
                'send_to': send_to,
            },
        )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        cart = ShoppingCart_Items.objects.filter(
            cart__owner=user,
            is_selected=True,
        )
        price = sum([item.quantity * item.item.price for item in cart])
        discount = ShoppingCart.objects.get(owner=user).discount
        if discount:
            total_cost = int(price - (price * discount) / 100)
        else:
            total_cost = price
        order = Order.objects.create(
            user=user,
            pay_method=validated_data.get('pay_method'),
            send_to=validated_data.get('send_to'),
            total_cost=total_cost,
        )
        for item in cart:
            OrderProductList.objects.create(
                order=order,
                product=item.item,
                quantity=item.quantity,
            )
        ShoppingCart_Items.objects.filter(cart__owner=user).delete()
        user_cart = ShoppingCart.objects.get(owner=user)
        user_cart.discount = None
        user_cart.save()
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
            'created',
            'product_list',
        )
        read_only_fields = (
            'id',
            'user',
            'product_list',
            'total_cost',
            'is_paid',
            'is_active',
            'number_order',
            'created',
            'modified',
        )
