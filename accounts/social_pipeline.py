from accounts.models import Account
from persons.models import AssociatedPerson, UserProfile, TypeOfDocument
from django.db import transaction


def create_account_user(strategy, details, backend, uid, user=None, *args, **kwargs):
    """
    Создает объект Account, если он не найден.
    """
    print(f"""create_account_user {details} {user}""")

    if user:
        return {"user": user}

    email = details.get("email")
    first_name = details.get("first_name", "")
    last_name = details.get("last_name", "")

    if not email:
        return

    try:
        user = Account.objects.get(email=email)
        return {"user": user}
    except Account.DoesNotExist:
        pass

    with transaction.atomic():
        user = Account.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=Account.objects.make_random_password(),  # случайный пароль
        )
        user.is_active = True  # Google уже подтвердил email
        user.save()

        # Создание связанного AssociatedPerson
        default_doc_type = TypeOfDocument.objects.first()
        associated = AssociatedPerson.objects.create(
            user_owner=user,
            first_name=first_name,
            last_name=last_name,
            type_of_document=default_doc_type,
            georgian_phone_number="",
            is_approved=True,
        )
        user.associated_person = associated
        user.save()

        # Создание профиля
        UserProfile.objects.create(
            user=user,
            person=associated,
        )

    return {"user": user}
