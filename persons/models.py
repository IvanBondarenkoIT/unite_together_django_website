from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

import re

from accounts.models import Account
from web_pages.models import WebContentObject, City, Events


class TypeOfDocument(models.Model):
    name = models.CharField(max_length=100)
    regex = models.CharField(max_length=100)
    hint = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Person(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class Country(models.TextChoices):
        Ukraine = 'Ukraine', 'Ukraine'
        Georgia = 'Georgia', 'Georgia'
        OTHER = 'Other', 'Other'

    user_owner = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    # is_default = models.BooleanField(default=False)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # slug = models.SlugField(max_length=200, blank=True)

    # Date of Birth
    date_of_birth = models.DateField(blank=True, null=True)
    # Citizenship
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    # Date of arrival
    date_of_arrival = models.DateField(blank=True, null=True)
    # Type of document
    # type_of_document = models.CharField(max_length=100, blank=True, null=True)
    type_of_document = models.ForeignKey(TypeOfDocument, on_delete=models.CASCADE, blank=True, null=True)
    # Document number
    document_number = models.CharField(max_length=20, blank=True, null=True)
    # document_number = models.CharField(max_length=50, blank=True, null=True)

    gender = models.CharField(max_length=3, choices=Gender.choices, blank=True, null=True)

    georgian_phone_number = models.CharField(max_length=50, blank=True, null=True)
    ukrainian_phone_number = models.CharField(max_length=50, blank=True, null=True)

    country = models.CharField(max_length=7, choices=Country.choices, blank=True, null=True)
    # city = models.CharField(max_length=50, blank=True, null=True)
    chosen_city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    address_line = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    edit_permission = models.BooleanField(default=True)

    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AssociatedPerson(Person):
    # unique_identifier = models.CharField(max_length=15, unique=True, blank=True, null=True, editable=False)
    unique_identifier = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.unique_identifier} {self.first_name} {self.last_name}"


@receiver(pre_save, sender=AssociatedPerson)
def set_unique_identifier(sender, instance, **kwargs):
    if not instance.unique_identifier:
        family_identifier = instance.user_owner.family_identifier

        if AssociatedPerson.objects.filter(user_owner=instance.user_owner).exists():

            all_family = AssociatedPerson.objects.filter(user_owner=instance.user_owner).order_by('unique_identifier')
            print(f"TEST  {[i.unique_identifier for i in list(all_family)]}")
            last_of_all_family_unique_identifier = [i.unique_identifier for i in list(all_family)][-1::]
            print(last_of_all_family_unique_identifier)
            person_number = int(last_of_all_family_unique_identifier[0][-2::])
            print(person_number)
            # person_number = all_family.count() + 1
            person_number += 1
            # Check is exist AssociatedPerson with the same number and try +1 to unique_identifier
            try:
                all_family.get(unique_identifier=f'GE{family_identifier}-{person_number:02d}')
                person_number += 1
            except:
                pass

        else:
            # Its first persson in this family
            person_number = 1

        # Reformat the  person_number
        person_identifier = f'{person_number:02d}'
        # Create new unique_identifier formated as example GE00001-01
        instance.unique_identifier = f'GE{family_identifier}-{person_identifier}'


class Participant(Person):
    copy_of_unique_identifier = models.CharField(max_length=15, blank=True, null=True, editable=False)
    class Status(models.TextChoices):
        REGISTERED = 'Registered', 'Registered'
        CANCELED = 'Canceled', 'Canceled'
        VISITED = 'Visited', 'Visited'

    registered_on = models.ForeignKey(Events, on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(max_length=10, choices=Status.choices, blank=True, null=True)

    def __str__(self):
        # return f"{self.first_name} {self.last_name} {self.registered_on.name}"
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.type_of_document and self.document_number:
            pattern = self.type_of_document.regex
            if not re.match(pattern, self.document_number):
                raise ValidationError(
                    {'document_number': 'Invalid document number format for the selected document type.'})


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    person = models.OneToOneField(AssociatedPerson, on_delete=models.CASCADE)
