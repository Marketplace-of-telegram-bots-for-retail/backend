from django.db.models import Avg

from products.models import Favorite, Order, Review, ShoppingCart


def find_rating(product_id):
    review = Review.objects.filter(product=product_id)
    if review.exists():
        return [
            round(review.aggregate(Avg('rating'))['rating__avg'], 1),
            review.count(),
        ]
    return [None, None]


def check_is_favorited(user, product_id):
    if user.is_anonymous:
        return False
    return Favorite.objects.filter(
        user=user,
        product=product_id,
    ).exists()


def check_is_in_shopping_cart(user, product_id):
    if user.is_anonymous:
        return False
    return ShoppingCart.objects.filter(
        owner=user,
        shoppingcart_items__item=product_id,
    ).exists()


def check_is_buying(user, product_id):
    if user.is_anonymous:
        return False
    return Order.objects.filter(
        user=user,
        product_list__order_with_product__product=product_id,
        is_paid=True,
    ).exists()
