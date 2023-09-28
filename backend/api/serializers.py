from rest_framework import serializers

from api.fields import Base64ImageField

# from core.utils import checking_existence
# from django.db.models import Avg
from products.models import Category, Product


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
