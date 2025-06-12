from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from persons.models import AssociatedPerson


class MyAccountManager(BaseUserManager):
    """
    Custom user manager.
    """

    def create_user(self, username, email, first_name="", last_name="", password=None):
        """
        Creates a user with the given parameters.
        """
        if not email:
            raise ValueError("Необхідно вказати адресу електронної пошти")
        if not username:
            raise ValueError("Необхідно встановити ім'я користувача")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """
        Creates a superuser with the given parameters.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """
    Custom user model.
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # family_identifier = models.CharField(max_length=10, unique=True, blank=True, null=True, editable=False)
    family_identifier = models.CharField(max_length=10, blank=True, null=True)
    associated_person = models.OneToOneField(
        "persons.AssociatedPerson", on_delete=models.CASCADE, blank="True", null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


@receiver(post_save, sender=Account)
def set_family_identifier(sender, instance, created, **kwargs):
    """
    Sets the family identifier for newly created users.
    """
    if created and not instance.family_identifier:
        last_identifier = (
            Account.objects.exclude(family_identifier__isnull=True)
            .order_by("-family_identifier")
            .first()
        )
        if last_identifier and last_identifier.family_identifier:
            next_id = int(last_identifier.family_identifier) + 1
        else:
            next_id = 1
        instance.family_identifier = f"{next_id:05d}"
        instance.save()


# models.py


# @receiver(post_migrate)
# def create_user_roles(sender, **kwargs):
#     coordinator_group, created = Group.objects.get_or_create(name='Coordinator')
#     supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
#
#     # Assign permissions to groups
#     # Coordinator permissions
#     coordinator_permissions = [
#         Permission.objects.get(codename='view_event'),
#         Permission.objects.get(codename='add_event'),
#         Permission.objects.get(codename='change_event'),
#         Permission.objects.get(codename='delete_event'),
#         Permission.objects.get(codename='view_participant'),
#         Permission.objects.get(codename='add_participant'),
#         Permission.objects.get(codename='change_participant'),
#         Permission.objects.get(codename='delete_participant'),
#     ]
#     coordinator_group.permissions.set(coordinator_permissions)
#
#     # Supervisor permissions (all Coordinator permissions + Person management)
#     supervisor_permissions = coordinator_permissions + [
#         Permission.objects.get(codename='view_person'),
#         Permission.objects.get(codename='add_person'),
#         Permission.objects.get(codename='change_person'),
#         Permission.objects.get(codename='delete_person'),
#     ]
#     supervisor_group.permissions.set(supervisor_permissions)
