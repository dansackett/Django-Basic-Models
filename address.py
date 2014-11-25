from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Address(models.Model):
    """
    A basic address that doesn't make assumptions about which countr(y|ies) it's used for.
    """
    ADDRESS_CHOICE_HOME = 10
    ADDRESS_CHOICE_BUSINESS = 20
    ADDRESS_CHOICE_OTHER = 30

    ADDRESS_TYPE_CHOICES = (
        (ADDRESS_CHOICE_HOME, 'Home'),
        (ADDRESS_CHOICE_BUSINESS, 'Business'),
        (ADDRESS_CHOICE_OTHER, 'Other'),
    )
    address_type = models.PositiveSmallIntegerField(choices=ADDRESS_TYPE_CHOICES,
                                                    default=ADDRESS_CHOICE_HOME)
    street_1 = models.CharField(blank=False, max_length=127)
    street_2 = models.CharField(blank=True, max_length=127)
    street_3 = models.CharField(blank=True, max_length=127)
    city = models.CharField(blank=False, max_length=63)
    state_province = models.CharField(blank=False, max_length=63)
    postal_code = models.CharField(blank=True, max_length=15)
    country = models.CharField(blank=True, max_length=63)

    class Meta:
        verbose_name_plural = 'Addresses'
        verbose_name = 'Address'

    def __str__(self):
        return '{}: {}'.format(self.get_address_type_display(), self.single_line_address)

    @property
    def single_line_address(self):
        return ' '.join(self.address_as_list)

    @property
    def city_state(self):
        return ', '.join([field for field in (self.city, self.state_province) if field])

    @property
    def city_state_postal_code(self):
        return ' '.join([field for field in (self.city, self.state_province, self.postal_code) if field])

    @property
    def address_as_list(self):
        return [
            field for field in
            (self.street_1, self.street_2, self.street_3, self.city, self.state_province,
             self.postal_code, self.country) if field
        ]
