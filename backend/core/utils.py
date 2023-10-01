from products.models import Review


def checking_existence(user, object, model):
    if user.is_anonymous:
        return False
    if model == Review:
        return model.objects.filter(
            user=user,
            product=object.id,
            is_favorite=True,
        ).exists()
    else:
        return model.objects.filter(
            user=user,
            product=object.id,
        ).exists()
