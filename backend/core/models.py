from behaviors.behaviors import Timestamped
from django.db import models


class DefaultModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class TimestampedModel(DefaultModel, Timestamped):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('created').verbose_name = 'дата публикации'
        self._meta.get_field('modified').verbose_name = 'дата изменения'

    class Meta:
        abstract = True
        ordering = ('-created',)
