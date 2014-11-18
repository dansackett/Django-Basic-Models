from django.db import models
from django_extensions.db.fields import UUIDField


class CommonFieldsModelBase(models.Model):
    """
    this class just provides several base fields
    """
    # django-extensions required for UUIDField
    uuid = UUIDField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True