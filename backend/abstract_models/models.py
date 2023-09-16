import pgtrigger
from django.db.models import BooleanField, DateTimeField, Model


class AbstractBaseModel(Model):
    is_active = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True
        triggers = [
            pgtrigger.Trigger(
                name="catch_update_timestamp",
                operation=pgtrigger.Update,
                when=pgtrigger.Before,
                func="NEW.updated_at = now(); RETURN NEW;",
            )
        ]

