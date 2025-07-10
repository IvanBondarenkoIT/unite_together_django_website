from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

import datetime
import re

from accounts.models import Account
from web_pages.models import City, Events


class TypeOfDocument(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    regex = models.CharField(max_length=100, verbose_name="Регулярний вираз")
    hint = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Підказка"
    )

    def __str__(self):
        return self.name


class Person(models.Model):
    class Gender(models.TextChoices):
        MALE = "Чоловік", "Чоловік"
        FEMALE = "Жінка", "Жінка"
        # Prohibited choice, as prohibited by Georgian legislation
        # OTHER = "Інше", "Інше"

    class Country(models.TextChoices):
        Georgia = "Грузія", "Грузія"

    class CitizenshipChoices(models.TextChoices):
        GEORGIAN = "Грузинське", "Грузинське"
        UKRAINIAN = "Українське", "Українське"
        OTHER = "Інше", "Інше"

    class Criteria(models.TextChoices):
        A = (
            "A",
            "A - Тяжко хворі, з інвалідністю чи обмеженими можливостями (з наявними в документами)",
        )
        B = "B", "B - Старше 60 років (за датою народження)"
        C = "C", "C - Багатодітна родина (3 та більше дитини до 18 років)"
        D = "D", "D - Одинока мати/ батько, що самостійно виховує неповнолітніх дітей"
        E = "E", "E - Жоден з вищеперечислених критеріїв не підходить"

    user_owner = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Ім'я Власника акаунту",
    )
    first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Ім'я (Латиниця)"
    )
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Прізвище (Латиниця)"
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Дата народження"
    )

    def get_current_age(self):
        """
        Calculates the current age in full years.
        """
        if not self.date_of_birth:
            return 0  # or another default if date_of_birth is not set

        today = (
            datetime.date.today()
        )  # Use datetime.date.today() if importing datetime as a whole
        years_difference = today.year - self.date_of_birth.year

        # Check if the birthday has occurred this year
        if (today.month, today.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            years_difference -= 1

        return years_difference

    citizenship = models.CharField(
        max_length=20,
        choices=CitizenshipChoices.choices,
        default=CitizenshipChoices.GEORGIAN,
        blank=True,
        null=True,
        verbose_name="Громадянство",
    )
    date_of_arrival = models.DateField(
        blank=True, null=True, verbose_name="Дата прибуття"
    )
    type_of_document = models.ForeignKey(
        TypeOfDocument,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Тип документа",
    )
    document_number = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Номер документа"
    )
    gender = models.CharField(
        max_length=7,
        choices=Gender.choices,
        blank=True,
        null=True,
        verbose_name="Стать",
    )
    georgian_phone_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Грузинський номер телефону"
    )
    ukrainian_phone_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Український номер телефону"
    )
    country = models.CharField(
        max_length=7,
        choices=Country.choices,
        default=Country.Georgia,
        blank=True,
        null=True,
        verbose_name="Країна",
    )
    chosen_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Вибране місто",
    )
    address_line = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Адреса"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def formatted_created_at(self):
        return self.created_at.strftime("%d.%m.%Y %H:%M")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    edit_permission = models.BooleanField(
        default=True, verbose_name="Дозвіл на редагування"
    )
    is_approved = models.BooleanField(default=True, verbose_name="Схвалено")

    criteria = models.CharField(
        default="E",
        max_length=1,
        choices=Criteria.choices,
        blank=True,
        null=True,
        verbose_name="Критерій",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AssociatedPerson(Person):
    unique_identifier = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Унікальний ідентифікатор"
    )

    def __str__(self):
        return f"{self.unique_identifier} {self.first_name} {self.last_name}"


@receiver(pre_save, sender=AssociatedPerson)
def set_unique_identifier(sender, instance, **kwargs):
    if not instance.unique_identifier:
        family_identifier = instance.user_owner.family_identifier

        if AssociatedPerson.objects.filter(user_owner=instance.user_owner).exists():
            all_family = AssociatedPerson.objects.filter(
                user_owner=instance.user_owner
            ).order_by("unique_identifier")
            last_of_all_family_unique_identifier = [
                i.unique_identifier for i in list(all_family)
            ][-1::]
            person_number = int(last_of_all_family_unique_identifier[0][-2::]) + 1

            try:
                all_family.get(
                    unique_identifier=f"GE{family_identifier}-{person_number:02d}"
                )
                person_number += 1
            except:
                pass

        else:
            person_number = 1

        person_identifier = f"{person_number:02d}"
        instance.unique_identifier = f"GE{family_identifier}-{person_identifier}"


class Participant(Person):
    copy_of_unique_identifier = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        editable=False,
        verbose_name="Копія унікального ідентифікатора",
    )

    class Status(models.TextChoices):
        REGISTERED = "Зареєстрований", "Зареєстрований"
        CANCELED = "Скасовано", "Скасовано"
        VISITED = "Відвідали", "Відвідали"

    # на какой Евент зарегистрирован участник
    registered_on = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Зареєстровано на",
    )
    # Статус регистрации От
    status = models.CharField(
        max_length=14,
        choices=Status.choices,
        blank=True,
        null=True,
        verbose_name="Статус",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.type_of_document and self.document_number:
            pattern = self.type_of_document.regex
            if not re.match(pattern, self.document_number):
                raise ValidationError(
                    {
                        "document_number": "Недійсний формат номера документа для вибраного типу документа"
                    }
                )


class UserProfile(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, verbose_name="Користувач"
    )
    person = models.OneToOneField(
        AssociatedPerson, on_delete=models.CASCADE, verbose_name="Пов'язана особа"
    )
