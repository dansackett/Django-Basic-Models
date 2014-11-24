from django_extensions.db.fields import UUIDField
from django_extensions.db.models import TimeStampedModel


class CommonFieldsModelBase(TimeStampedModel):
    """
    this class just provides several base fields
    uuid: a uuid4 field
    created: creation timestamp (from TimeStampModel)
    modified: modified timestamp (from TimeStampModel)
    """
    uuid = UUIDField()

    class Meta:
        abstract = True