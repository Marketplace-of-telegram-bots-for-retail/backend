def checking_existence(user, object, model):
    if user.is_anonymous:
        return False
    return model.objects.filter(
        user=user,
        product_id=object.id,
    ).exists()
