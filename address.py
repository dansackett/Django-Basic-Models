from django.db import models


class Address(models.Model):
    """
    A basic address that doesn't make assumptions about which countr(y|ies) it's used for.
    """
    ADDRESS_TYPE_CHOICES = (
        (1, 'Home'),
        (2, 'Business'),
        (3, 'Other'),
    )
    ADDRESS_TYPE_DEFAULT = 1
    address_type = models.PositiveSmallIntegerField(null=False, choices=ADDRESS_TYPE_CHOICES,
                                                    default=ADDRESS_TYPE_DEFAULT)

    street_1 = models.CharField(blank=False, max_length=127)
    street_2 = models.CharField(blank=True, max_length=127)
    street_3 = models.CharField(blank=True, max_length=127)
    city = models.CharField(blank=False, max_length=63)
    state_province = models.CharField(blank=False, max_length=63)
    postal_code = models.CharField(blank=True, max_length=15)
    country = models.CharField(blank=True, max_length=63)

    class Meta:
        abstract = True
        verbose_name_plural = u'Addresses'
        verbose_name = u'Address'

    def __str__(self):
        return u'%s: %s' % (self.get_address_type_display(), self.single_line_address)

    @property
    def single_line_address(self):
        return u' '.join(self.address_as_list)

    @property
    def city_state(self):
        return u', '.join([field for field in (self.city, self.state_province) if field])

    @property
    def city_state_postal(self):
        return u' '.join([field for field in (self.city, self.state_province, self.postal_code) if field])

    @property
    def address_as_list(self):
        return [
            field for field in
            (self.street_1, self.street_2, self.street_3, self.city, self.state_province,
             self.postal_code, self.country) if field
        ]