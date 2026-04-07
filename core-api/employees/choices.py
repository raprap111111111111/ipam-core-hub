from django.db import models
from django.utils.translation import gettext_lazy as _

class EmployeeStatus(models.TextChoices):
    ACTIVE = 'active', _('Active')
    ON_LEAVE = 'on_leave', _('On Leave')
    TERMINATED = 'terminated', _('Terminated')
    RESIGNED = 'resigned', _('Resigned')

class EmployeeType(models.TextChoices):
    REGULAR = 'regular', _('Regular')
    PROBATIONARY = 'probationary', _('Probationary')
    CONTRACTUAL = 'contractual', _('Contractual')
    INTERN = 'intern', _('Intern')

class Gender(models.TextChoices):
    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')
    OTHER = 'other', _('Other')
    PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer not to say')