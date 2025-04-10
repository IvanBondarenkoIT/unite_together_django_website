from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

# from django.contrib.auth.password_validation import validate_password

from unite_together_django_website.validators import CustomPasswordValidator
from .models import UserProfile, AssociatedPerson, Participant
from accounts.models import Account
from .forms import AssociatedPersonForm

OBJECTS_ON_PAGE = 4


@login_required(login_url="login")
def associated_person_list(request, lang="uk"):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Данные о последнем евенте
    last_event = request.session.get("last_event")

    persons = AssociatedPerson.objects.filter(user_owner=user_profile.user).order_by(
        "unique_identifier"
    )
    main_person = user_profile.user.associated_person
    context = {
        "persons": persons,
        "main_person": main_person,
        "last_event": last_event,
    }

    return render(
        request,
        "persons/associated_person_list.html",
        context=context,
    )


@login_required(login_url="login")
def associated_person_create(request, lang="uk"):
    if request.method == "POST":
        form = AssociatedPersonForm(
            request.POST,
            default_ge_phone=request.user.associated_person.georgian_phone_number,
            user=request.user,
        )
        if form.is_valid():
            associated_person = form.save(commit=False)
            associated_person.user_owner = request.user
            associated_person.is_active = True
            associated_person.is_approved = True  # Later can be manual approval
            associated_person.save()

            # Проверяем, какая кнопка была нажата
            if "save_and_continue" in request.POST:
                messages.success(
                    request, "Особа збережена, додайте наступного члена родини."
                )
                return redirect("associated_person_create")  # Открыть новую форму
            else:
                messages.success(request, "Особа успішно створена!")
                return redirect("associated_person_list")  # Перейти к списку
        else:
            messages.error(request, "Будь ласка, виправте помилки нижче.")
    else:
        form = AssociatedPersonForm(
            default_ge_phone=request.user.associated_person.georgian_phone_number,
            user=request.user,
        )

    return render(request, "persons/dashboard.html", {"form": form})


@login_required(login_url="login")
def associated_person_edit(request, pk, lang="uk"):
    edited_person = get_object_or_404(AssociatedPerson, pk=pk)

    if request.method == "POST":
        form = AssociatedPersonForm(
            request.POST,
            instance=edited_person,
            default_ge_phone=request.user.associated_person.georgian_phone_number,
            user=request.user,
        )
        if form.is_valid():
            associated_person = form.save(commit=False)
            associated_person.is_approved = True  # Later can be manual approval
            associated_person.save()

            # Проверяем, какая кнопка была нажата
            if "save_and_continue" in request.POST:
                messages.success(
                    request, "Особа збережена, додайте наступного члена родини."
                )
                return redirect("associated_person_create")  # Открыть новую форму
            else:
                messages.success(request, "Ваш профіль було оновлено.")
                return redirect("associated_person_list")  # Перейти к списку
        else:
            messages.error(request, "Будь ласка, виправте помилки нижче.")
    else:
        form = AssociatedPersonForm(
            instance=edited_person,
            default_ge_phone=request.user.associated_person.georgian_phone_number,
            user=request.user,
        )

    return render(request, "persons/dashboard.html", {"form": form})


@login_required(login_url="login")
def registered_events(request, lang="uk"):
    participants = (
        Participant.objects.all()
        .filter(user_owner=request.user)
        .order_by("-created_at")
    )

    # Pagination functional
    paginator = Paginator(participants, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)

    # Get count efficiently / faster
    objects_count = paginator.count

    context = {"participants": page_all_objects, "objects_count": objects_count}
    return render(request, "persons/personal-account-events.html", context=context)


@login_required(login_url="login")
def settings(request, lang="uk"):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            if user.check_password(current_password):
                try:
                    # Validate the new password using Django's built-in validators
                    # validate_password(new_password, user)

                    # Custom password validator (if any)
                    password_validator = CustomPasswordValidator()
                    password_validator.validate(new_password)

                    # If no exception is raised, set the new password
                    user.set_password(new_password)
                    user.save()

                    # Update session to prevent logout
                    update_session_auth_hash(request, user)

                    messages.success(request, "Пароль успішно оновлено.")
                    return redirect("settings")
                except ValidationError as e:
                    # Catching multiple error messages and adding them to the messages framework
                    for error in e:
                        messages.error(request, error)
                    return redirect("settings")
            else:
                messages.error(
                    request, "Будь ласка, введіть правильний поточний пароль"
                )
                return redirect("settings")
        else:
            messages.error(request, "Паролі не збігаються")
            return redirect("settings")
    else:
        return render(request, "persons/personal-account-settings.html")
