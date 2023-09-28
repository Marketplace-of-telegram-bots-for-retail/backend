from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.models import Review, Product


class ReviewSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(
		default=serializers.CurrentUserDefault(),
		slug_field='username',
		read_only=True
	)
	product = serializers.SlugRelatedField(
		slug_field='name',
		read_only=True
	)

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
		exclude = ['is_active', ]


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
		return Review.objects.filter(user=request.user, product=obj).exists()
