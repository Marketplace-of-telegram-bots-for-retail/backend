from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.fields import Base64ImageField

# from core.utils import checking_existence
# from django.db.models import Avg
from products.models import Category, Product, Review


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

    def get_rating(self, object):
        # review = Review.objects.filter(product_id=object.id)
        # if review.exists():
        #      return [
        #         round(review.aggregate(Avg('rating'))['rating__avg'], 1),
        #         review.count(),
        #      ]
        return [None, None]

    def get_is_favorited(self, object):
        # return checking_existence(
        #     self.context.get('request').user,
        #     object,
        #     Favorite,
        # )
        return None

    def get_is_in_shopping_cart(self, object):
        # return checking_existence(
        #     self.context.get('request').user,
        #     object,
        #     ShoppingCart,
        # )
        return None


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    def validate_review(self, data):
        request = self.context['request']
        user = request.user
        product_id = self.context['view'].kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        if request.method == 'POST':
            if Review.objects.filter(product=product, user=user).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили свой отзыв к этому товару!'
                )
        return data

    def validate_favorite(self, data):
        request = self.context.get('request')
        product = data['product']
        if Review.objects.filter(user=request.user, product=product).exists():
            raise serializers.ValidationError(
                {'errors': 'Этот товар уже в избранном!'}
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Выберите значение от 1 до 5')
        return value

    def create(self, validated_data):
        user = self.context.get('request').user
        review = Review.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ReviewListSerializer(instance, context=context).data

    class Meta:
        model = Review
        exclude = [
            'is_active',
        ]


class ReviewListSerializer(serializers.ModelSerializer):
    # user = CustomUserSerializer(read_only=True)
    products = serializers.SerializerMethodField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def get_reviews(self, obj):
        queryset = Review.objects.filter(product=obj)
        return ReviewSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Review.objects.filter(
            user=request.user, product=obj, is_favorite=True
        ).exists()
