from django.core.exceptions import ValidationError

from products.models import ShoppingCart_Items


def validate_pay_method(pay_method):
    if not pay_method:
        raise ValidationError({'message': 'Укажите метод оплаты заказа.'})
    if pay_method not in ['card', 'sbp']:
        raise ValidationError({'message': 'Недопустимый метод оплаты заказа.'})


def validate_send_to(send_to, context):
    request = context.get('request')
    if not send_to:
        return request.user.email
    return send_to


# def validate_order(context):
#     user = context.get('request').user
#     order = Order.objects.filter(user=user, is_paid=False)
#     if order:
#         raise ValidationError(
#             {
#                 'message': 'У вас уже есть неоплаченный заказ, оплатите '
#                 'или удалите его.',
#             },
#         )
# Пока убрал ограничение в 1 неоплаченный заказ


def validate_cart(context):
    user = context.get('request').user
    cart = ShoppingCart_Items.objects.filter(
        cart__owner=user,
        is_selected=True,
    )
    if cart:
        return True
    raise ValidationError({'message': 'Ваша корзина пуста.'})
