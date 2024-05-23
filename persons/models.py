from django.db import models
from accounts.models import Account
from web_pages.models import WebContentObject


# GENDER_CHOICES = [
#     ('M', 'Male'),
#     ('F', 'Female'),
#     ('NB', 'Non-Binary'),
#     ('O', 'Other'),
#     ('PNS', 'Prefer not to say'),
# ]


# Create your models here.
class Person(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
    #     OTHER = 'O', 'Other'
    #     NON_BINARY = 'NB', 'Non-Binary'
        PREFER_NOT_TO_SAY = 'PNS', 'Prefer not to say'

    user_owner = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
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
    type_of_document = models.CharField(max_length=100, blank=True, null=True)
    # Document number
    document_number = models.IntegerField(blank=True, null=True)

    gender = models.CharField(max_length=3, choices=Gender.choices)

    georgian_phone_number = models.CharField(max_length=50, blank=True, null=True)
    ukrainian_phone_number = models.CharField(max_length=50, blank=True, null=True)

    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    address_line = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    # is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.user_owner.email}"


class Participant(Person):
    registered_on = models.ForeignKey(WebContentObject, on_delete=models.CASCADE, blank=True, null=True)
