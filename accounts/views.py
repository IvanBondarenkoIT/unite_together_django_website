from django.db import transaction
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import RegistrationForm, PhoneForm
from accounts.models import Account
from persons.models import UserProfile, AssociatedPerson, TypeOfDocument
from unite_together_django_website.validators import CustomPasswordValidator

from django.core.mail import send_mail
from decouple import config
from django.http import HttpResponse


def register(request, lang="uk"):
    """
    Handles user registration.

    - If the request method is POST and the form is valid, it creates a new user and
      associated profile and sends an activation email.
    - If registration is successful, redirects to the login page with a verification message.
    - If GET, it renders the registration form.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HTTPResponse: Redirects or renders the registration page based on request method.
    """
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

                    # Create new associated person record
                    default_document_type = TypeOfDocument.objects.first()
                    new_person = AssociatedPerson.objects.create(
                        user_owner=user,
                        first_name=first_name,
                        last_name=last_name,
                        type_of_document=default_document_type,
                        georgian_phone_number=phone_number,
                        is_approved=False,
                    )
                    new_person.save()

                    user.associated_person = new_person
                    user.phone_number = phone_number
                    user.save()

                    # Create user profile
                    profile = UserProfile.objects.create(
                        user=user,
                        person=new_person,
                    )
                    profile.save()

                    messages.success(
                        request,
                        (
                            "Профіль успішно створено"
                            if lang == "uk"
                            else "Profile created successfully!"
                        ),
                    )

                    # Send activation email
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
                    # send_email = EmailMessage(mail_subject, message, to=[email])
                    # send_email.send()

                    # subject = "Тестовое письмо"
                    # message = "Привет! Это тестовое письмо для проверки SMTP-конфигурации."
                    from_email = config("EMAIL_ADMIN")
                    recipient_list = [email]  # Замените на ваш email для тестирования

                    mail_sent = False
                    max_attempts = 5
                    attempts = 0

                    while not mail_sent and attempts < max_attempts:
                        try:
                            send_mail(mail_subject, message, from_email, recipient_list)
                            mail_sent = True  # Email sent successfully
                        except Exception as e:
                            attempts += 1  # Increment the attempt counter
                            if attempts >= max_attempts:
                                messages.error(
                                    request,
                                    (
                                        "Не вдалося надіслати лист для активації. Спробуйте ще раз пізніше."
                                        if lang == "uk"
                                        else "Failed to send activation email. Please try again later."
                                    ),
                                )

                    # Log the user in after successful registration
                    auth_login(request, user)
                    
                    # Show success message
                    messages.success(
                        request,
                        ("Ви успішно зареєструвалися та увійшли в систему!"
                         if lang == "uk"
                         else "You have successfully registered and logged in!")
                    )
                    
                    # Redirect to associated person's edit page
                    return redirect(f'/{lang}/persons/associated-persons/{new_person.id}/edit/')

            except Exception as e:
                messages.error(request, e)
                return redirect("register")
        else:
            messages.error(
                request, "Помилка реєстрації" if lang == "uk" else "Registration error"
            )
    else:
        form = RegistrationForm()

    context = {
        "form": form,
        "lang": lang,
    }

    return render(request, "accounts/register.html", context=context)


def login(request, lang="uk"):
    """
    Handles user login.

    - If the request method is POST, authenticates user with email and password.
    - If successful, redirects to the home page; otherwise, returns an error message.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HTTPResponse: Redirects or renders the login page based on success or failure.
    """
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

    return render(request, "accounts/login.html", context={"lang": lang})


@login_required(login_url="login")
def logout(request, lang="uk"):
    """
    Logs out the user and redirects to the login page.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HTTPResponse: Redirects to the login page with a success message.
    """
    auth.logout(request)
    messages.success(request, "Успішний вихід" if lang == "uk" else "Logout")
    # Do: Create the same if stance for all accounts views
    if lang == "uk":
        return redirect("login")
    else:
        return redirect("login_en", lang=lang)


def activate(request, uidb64, token, lang="uk"):
    """
    Activates user account via a verification link.

    - Decodes the uid and verifies the token.
    - If valid, activates the account and redirects to login with a success message.

    Parameters:
    - request: The HTTP request object.
    - uidb64 (str): Base64-encoded user ID.
    - token (str): Token for account verification.

    Returns:
    - HTTPResponse: Redirects based on activation success or failure.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            (
                "Щиро вітаю! Ваш обліковий запис активовано!"
                if lang == "uk"
                else "Congratulations! Your account has been activated!"
            ),
        )
        return redirect("login" if lang == "uk" else "login_en")
    else:
        messages.error(
            request,
            (
                "Недійсне посилання для активації"
                if lang == "uk"
                else "Invalid activation link"
            ),
        )
        return redirect("register" if lang == "uk" else "register_en")


def forgot_password(request, lang="uk"):
    """
    Initiates the password reset process.

    - If POST, checks if the user exists and sends a reset email.
    - If user does not exist, returns an error message.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HTTPResponse: Redirects or renders the forgot password page.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = (
                "Будь ласка, скиньте свій пароль"
                if lang == "uk"
                else "Please reset your password"
            )
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            # send_email = EmailMessage(mail_subject, message, to=[email])
            # send_email.send()
            from_email = config("EMAIL_ADMIN")
            recipient_list = [email]  # Замените на ваш email для тестирования

            try:
                send_mail(mail_subject, message, from_email, recipient_list)
                # return HttpResponse("Письмо успешно отправлено!")
            except Exception as e:
                messages.error(
                    "Не вдалося відправити лист"
                    if lang == "uk"
                    else "Failed to send email"
                )

            messages.success(
                request,
                (
                    "Лист для зміни пароля надіслано на вашу електронну адресу"
                    if lang == "uk"
                    else "Password reset email has been sent to your email address"
                ),
            )
            return redirect("login" if lang == "uk" else "login_en")

        else:
            messages.error(
                request,
                (
                    "Обліковий запис не існує"
                    if lang == "uk"
                    else "Account does not exist"
                ),
            )
            return redirect("forgot_password" if lang == "uk" else "forgot_password_en")

    return render(request, "accounts/forgot_password.html", context={"lang": lang})


def reset_password_validate(request, uidb64, token, lang="uk"):
    """
    Validates the reset password token and allows password reset.

    - Decodes the uid and checks the token.
    - If valid, redirects to reset password page.

    Parameters:
    - request: The HTTP request object.
    - uidb64 (str): Base64-encoded user ID.
    - token (str): Token for password reset.

    Returns:
    - HTTPResponse: Redirects based on token validity.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(
            request,
            (
                "Будь ласка, скиньте свій пароль"
                if lang == "uk"
                else "Please reset your password"
            ),
        )
        return redirect(
            "reset_password" if lang == "uk" else "reset_password_en" + "?lang=" + lang
        )
    else:
        messages.error(
            request,
            (
                "Термін дії цього посилання закінчився"
                if lang == "uk"
                else "This link has expired"
            ),
        )
        return redirect("login" if lang == "uk" else "login_en")


def reset_password(request, lang="uk"):
    """
    Handles the password reset form submission.

    - If POST, validates and sets the new password for the user.
    - If validation fails, returns error messages.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HTTPResponse: Redirects based on success or failure of the password reset.
    """
    if request.method == "POST":
        password = request.POST["new_password"]
        confirm_password = request.POST["confirm_new_password"]

        if password == confirm_password:
            uid = request.session.get("uid", None)
            user = Account.objects.get(pk=uid)
            try:
                # Custom password validator
                password_validator = CustomPasswordValidator()
                password_validator.validate(password)
                user.set_password(password)
                user.save()
                messages.success(
                    request,
                    (
                        "Скидання пароля успішне"
                        if lang == "uk"
                        else "Password reset successful"
                    ),
                )
                return redirect("login" if lang == "uk" else "login_en")
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
                return redirect(
                    "reset_password" if lang == "uk" else "reset_password_en"
                )
        else:
            messages.error(
                request,
                "Паролі не збігаються" if lang == "uk" else "Passwords do not match",
            )
            return redirect("reset_password" if lang == "uk" else "reset_password_en")
    else:
        return render(request, "accounts/reset_password.html", context={"lang": lang})


@login_required
def require_phone_view(request):
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            user_profile = get_object_or_404(UserProfile, user=request.user)
            user_profile.person.georgian_phone_number = phone_number
            user_profile.person.save()

            request.user.save()
            return redirect("associated_person_list")
    else:
        form = PhoneForm()
    return render(request, "accounts/require_phone.html", {"form": form})
