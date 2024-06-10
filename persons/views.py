from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile, AssociatedPerson, Participant
from accounts.models import Account
from .forms import AssociatedPersonForm, AssociatedPersonFormSet


OBJECTS_ON_PAGE = 4


@login_required(login_url="login")
def dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)  # Get UserProfile with user==request.user

    if request.method == "POST":
        person_form = AssociatedPersonForm(request.POST, request.FILES, instance=user_profile.person)
        if person_form.is_valid():
            person_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect("dashboard")
    else:
        person_form = AssociatedPersonForm(instance=user_profile.person)

    return render(request, "persons/dashboard.html", {'form': person_form})


@login_required(login_url="login")
def create_person(request):
    if request.method == 'POST':
        form = AssociatedPersonForm(request.POST)
        if form.is_valid():
            associated_person = form.save(commit=False)
            associated_person.user_owner = request.user
            associated_person.save()
            messages.success(request, 'Person created successfully!')
            return redirect('home')  # Change to your desired redirect target
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AssociatedPersonForm()

    return render(request, 'persons/create_person.html', {'form': form})


@login_required(login_url="login")
def person_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)  # Get UserProfile with user==request.user
    if request.method == 'POST':
        formset = AssociatedPersonFormSet(request.POST)
        if formset.is_valid():
            associated_person = formset.save(commit=False)
            associated_person.user_owner = request.user
            associated_person.save()
            messages.success(request, 'Person created successfully!')
            return redirect('person_list')  # Change to your desired redirect target
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        formset = AssociatedPersonFormSet(queryset=AssociatedPerson.objects.all().filter(is_active=True, user_owner=request.user))

    return render(request, 'persons/person_list.html', {'formset': formset})


# @login_required(login_url="login")
# def create_participant(request):
#     if request.method == 'POST':
#         form = ParticipantForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('participant_list')  # Change to your desired redirect target
#     else:
#         form = ParticipantForm()
#
#     return render(request, 'persons/create_participant.html', {'form': form})


# @login_required(login_url="login")
# def participant_list(request):
#     if request.method == 'POST':
#         formset = ParticipantFormSet(request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect('participant_list')  # Change to your desired redirect target
#     else:
#         formset = ParticipantFormSet(queryset=Participant.objects.all())
#
#     return render(request, 'persons/participant_list.html', {'formset': formset})


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


@login_required(login_url="login")
def settings(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated succesfully.")
                return redirect("change_password")
            else:
                messages.error(request, "Please enter correct password")
                return redirect("change_password")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("change_password")

    return render(request, 'persons/personal-account-settings.html')