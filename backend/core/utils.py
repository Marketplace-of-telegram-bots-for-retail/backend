def checking_existence(user, object, model):
    if user.is_anonymous:
        return False
    else:
        return model.objects.filter(
            user=user,
            product=object.id,
        ).exists()
