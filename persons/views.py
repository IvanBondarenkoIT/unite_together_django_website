from django.core.exceptions import ValidationError
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required

from unite_together_django_website.validators import CustomPasswordValidator
from .models import UserProfile, AssociatedPerson, Participant
from accounts.models import Account
from .forms import AssociatedPersonForm, AssociatedPersonFormSet



OBJECTS_ON_PAGE = 4


# @login_required(login_url="login")
# def dashboard(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)  # Get UserProfile with user==request.user
#
#     if request.method == "POST":
#         person_form = AssociatedPersonForm(request.POST, request.FILES, instance=user_profile.person)
#         if person_form.is_valid():
#             person_form.save()
#             messages.success(request, "Your profile has been updated")
#             return redirect("dashboard")
#     else:
#         person_form = AssociatedPersonForm(instance=user_profile.person)
#
#     return render(request, "persons/dashboard.html", {'form': person_form})


# @login_required(login_url="login")
# def create_person(request):
#     if request.method == 'POST':
#         form = AssociatedPersonForm(request.POST)
#         if form.is_valid():
#             associated_person = form.save(commit=False)
#             associated_person.user_owner = request.user
#             associated_person.is_active = True
#             associated_person.save()
#             messages.success(request, 'Person created successfully!')
#             return redirect("dashboard")
#         else:
#             messages.error(request, 'Please correct the errors below.')
#             return redirect("dashboard")
#     else:
#         form = AssociatedPersonForm()
#
#     return render(request, 'persons/create_person.html', {'form': form})


# @login_required(login_url="login")
# def person_list(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)  # Get UserProfile with user==request.user
#     if request.method == 'POST':
#         formset = AssociatedPersonFormSet(request.POST)
#         if formset.is_valid():
#             associated_person = formset.save(commit=False)
#             associated_person.user_owner = request.user
#             associated_person.is_active = True
#             associated_person.save()
#             messages.success(request, 'Person created successfully!')
#             return redirect('person_list')  # Change to your desired redirect target
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         formset = AssociatedPersonFormSet(queryset=AssociatedPerson.objects.all().filter(is_active=True, user_owner=request.user).order_by("unique_identifier"))
#
#     return render(request, 'persons/person_list.html', {'formset': formset})

@login_required(login_url="login")
def associated_person_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    persons = AssociatedPerson.objects.filter(user_owner=user_profile.user).order_by("unique_identifier")
    main_person = user_profile.user.associated_person
    return render(request, 'persons/associated_person_list.html', {'persons': persons, 'main_person': main_person})

@login_required(login_url="login")
def associated_person_create(request):
    if request.method == 'POST':
        # user_owner = request.user  # Assuming user is the owner
        form = AssociatedPersonForm(request.POST)
        if form.is_valid():
            associated_person = form.save(commit=False)
            associated_person.user_owner = request.user
            associated_person.is_active = True
            associated_person.save()
            messages.success(request, 'Person created successfully!')
            return redirect("associated_person_list")
        else:
            messages.error(request, 'Please correct the errors below.')
        #     return redirect("associated_person_create")
    else:
        form = AssociatedPersonForm()

    return render(request, 'persons/dashboard.html', {'form': form})

@login_required(login_url="login")
def associated_person_edit(request, pk):
    edited_person = AssociatedPerson.objects.get(pk=pk)

    if request.method == "POST":
        # user_owner = request.user  # Assuming user is the owner
        person_form = AssociatedPersonForm(request.POST, request.FILES, instance=edited_person)
        # person_form = AssociatedPersonForm(request.POST, instance=edited_person)
        if person_form.is_valid():
            person_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect("associated_person_list")

        else:
            messages.error(request, 'Please correct the errors below.')
        #     return redirect("associated_person_edit", pk=edited_person.pk)
    else:
        person_form = AssociatedPersonForm(instance=edited_person)

    return render(request, "persons/dashboard.html", {'form': person_form})





@login_required(login_url="login")
def registered_events(request):
    participants = Participant.objects.all().filter(user_owner=request.user).order_by('-created_at')

    # Pagination functional
    paginator = Paginator(participants, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)

    # Get count efficiently / faster
    objects_count = paginator.count

    context = {
        'participants': page_all_objects,
        'objects_count': objects_count
    }
    return render(request, 'persons/personal-account-events.html', context=context)


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required(login_url="login")
def settings(request):
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

                    messages.success(request, "Password updated successfully.")
                    return redirect("settings")
                except ValidationError as e:
                    # Catching multiple error messages and adding them to the messages framework
                    for error in e:
                        messages.error(request, error)
                    return redirect("settings")
            else:
                messages.error(request, "Please enter the correct current password")
                return redirect("settings")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("settings")
    else:
        return render(request, 'persons/personal-account-settings.html')

