from django.db import transaction

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import RegistrationForm
from accounts.models import Account
from persons.models import UserProfile, AssociatedPerson, TypeOfDocument
from unite_together_django_website.validators import CustomPasswordValidator


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email

            try:
                with transaction.atomic():
                    user = Account.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                        password=password,
                    )
                    user.save()

                    # Create new Person
                    default_document_type = TypeOfDocument.objects.first()

                    new_person = AssociatedPerson.objects.create(
                        user_owner=user,
                        first_name=first_name,
                        last_name=last_name,
                        type_of_document=default_document_type,
                        is_approved=False,
                    )
                    new_person.save()

                    user.associated_person = new_person
                    user.phone_number = phone_number
                    user.save()

                    # Create user Profile
                    profile = UserProfile.objects.create(
                        user=user,
                        person=new_person,
                    )
                    profile.save()

                    messages.success(request, "Профіль успішно створено ")

                    # USER ACTIVATION
                    current_site = get_current_site(request)
                    mail_subject = "Please activate your account"
                    message = render_to_string(
                        "accounts/account_verification_email.html",
                        {
                            "user": user,
                            "domain": current_site.domain,
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": default_token_generator.make_token(user),
                        },
                    )
                    to_email = email
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.send()

                    # messages.success(request, "Registration Successful")
                    return redirect(
                        f"/accounts/login/?command=verification&email={email}"
                    )

            except Exception as e:
                messages.error(request, e)
                return redirect("register")

    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/register.html", context=context)


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Успішний вхід")
            return redirect("home")
        else:
            messages.error(request, "Недійсні облікові дані для входу")
            return redirect("login")

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "Успішний вхід")
    return redirect("login")


def activate(request, uidb64, token):
    # return HttpResponse("OK")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Щиро вітаю! Ваш обліковий запис активовано!")
        return redirect("login")
    else:
        messages.error(request, "Недійсне посилання для активації")
        return redirect("Register")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = "Будь ласка, скиньте свій пароль"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "Лист для зміни пароля надіслано на вашу електронну адресу"
            )

            return redirect("login")

        else:
            messages.error(request, "Обліковий запис не існує")
            return redirect("forgot_password")

    return render(request, "accounts/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        # request.user.is_active = True
        user.save()
        messages.success(request, "Будь ласка, скиньте свій пароль")
        return redirect("reset_password")
    else:
        messages.error(request, "Термін дії цього посилання закінчився")
        return redirect("login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid", None)
            user = Account.objects.get(pk=uid)
            try:
                # Custom password validator
                password_validator = CustomPasswordValidator()
                password_validator.validate(password)
                user.set_password(password)
                user.save()
                messages.success(request, "Скидання пароля успішне")
                return redirect("login")
            except ValidationError as e:
                # Catching multiple error messages and adding them to the messages framework
                for error in e:
                    messages.error(request, error)
                return redirect("reset_password")
        else:
            messages.error(request, "Паролі не збігаються")
            return redirect("reset_password")
    else:
        return render(request, "accounts/reset_password.html")
