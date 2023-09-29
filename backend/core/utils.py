def checking_existence(user, object, model):
    if user.is_anonymous:
        return False
    return model.objects.filter(
        user=user,
        product_id=object.id,
    ).exists()


def user_directory_path(instance, filename):
    return f'products/{instance.user.username}/{filename}'
