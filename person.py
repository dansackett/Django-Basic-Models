from django.db import models
from datetime import date


class Person(models.Model):
    """
    A relatively simple Person model
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    first_name = models.CharField(max_length=31, blank=False)
    middle_name = models.CharField(max_length=31, blank=True)
    last_name = models.CharField(max_length=31, blank=False)

    prefix = models.CharField(blank=True, max_length=31)
    suffix = models.CharField(blank=True, max_length=31)
    suffix_requires_comma = models.BooleanField(default=True, help_text="Some suffixes like 'Jr.' require a commna, "
                                                                        "while others, such as 'III', don't.")

    gender = models.CharField(null=True, max_length=1, blank=True, choices=GENDER_CHOICES)

    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('last_name', 'first_name', 'middle_name')
        verbose_name_plural = 'People'

    def __str__(self):
        return self.full_name_forward

    def _get_full_name(self, last_name_first=False, include_middle_name=False):
        if last_name_first:
            return ', '.join([name for name in (self.get_last_name_with_suffix(),
                                                self.get_first_name_with_prefix(include_middle_name=include_middle_name)
                                                ) if name])
        else:
            return ' '.join([name for name in (self.get_first_name_with_prefix(include_middle_name=include_middle_name),
                                               self.get_last_name_with_suffix()) if name])

    def get_first_name_with_prefix(self, include_middle_name=False):
        """

        :param include_middle_name: if True, will include the middle name
        :return: <prefix> <firstname> <middlename (if included)>
        """
        name_list = [self.prefix, self.first_name]
        if include_middle_name:
            name_list.append(self.middle_name)
        return ' '.join([name for name in name_list if name])

    def get_last_name_with_suffix(self):
        """

        :return: <lastname>, <suffix>
        """
        join_str = ', ' if self.suffix_requires_comma else ' '
        return join_str.join([name for name in (self.last_name, self.suffix) if name])

    @property
    def full_name_forward(self):
        return self._get_full_name(last_name_first=False)

    @property
    def full_name_forward_with_middle_name(self):
        return self._get_full_name(last_name_first=False, include_middle_name=True)

    @property
    def full_name_backward(self):
        return self._get_full_name(last_name_first=True)

    @property
    def full_name_backward_with_middle_name(self):
        return self._get_full_name(last_name_first=True, include_middle_name=True)

    def get_birth_death_span(self, date_format='%b. %d %Y'):
        birth = self.birth_date.strftime(date_format) if self.birth_date else None
        death = self.death_date.strftime(date_format) if self.death_date else None

        if birth and death:
            return '{} - {}'.format(birth, death)
        elif birth:
            return 'b. {}'.format(birth)
        elif death:
            return 'd. {}'.format(death)
        else:
            return ''

    @property
    def age(self):
        """

        :return: an integer
        """
        if not self.birth_date:
            return None

        today = date.today()
        try:
            birthday = self.birth_date.replace(year=today.year)
        except ValueError:  # raised when birth_date is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=today.year, month=born.month + 1, day=1)

        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year