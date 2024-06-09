from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile, AssociatedPerson
from .forms import AssociatedPersonForm, ParticipantForm
from .forms import AssociatedPersonFormSet, ParticipantFormSet

from .models import Person, Participant

OBJECTS_ON_PAGE = 1

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


    return render(request, "accounts/dashboard.html", {'form': person_form})

@login_required(login_url="login")
def create_person(request):
    if request.method == 'POST':
        form = AssociatedPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Change to your desired redirect target
    else:
        form = AssociatedPersonForm()

    return render(request, 'persons/create_person.html', {'form': form})


@login_required(login_url="login")
def person_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)  # Get UserProfile with user==request.user
    if request.method == 'POST':
        formset = AssociatedPersonFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('person_list')  # Change to your desired redirect target
    else:
        formset = AssociatedPersonFormSet(queryset=AssociatedPerson.objects.all().filter(is_active=True, user_owner=request.user))

    return render(request, 'persons/person_list.html', {'formset': formset})


@login_required(login_url="login")
def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')  # Change to your desired redirect target
    else:
        form = ParticipantForm()

    return render(request, 'persons/create_participant.html', {'form': form})


@login_required(login_url="login")
def participant_list(request):
    if request.method == 'POST':
        formset = ParticipantFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('participant_list')  # Change to your desired redirect target
    else:
        formset = ParticipantFormSet(queryset=Participant.objects.all())

    return render(request, 'persons/participant_list.html', {'formset': formset})


@login_required(login_url="login")
def settings(request):
    return render(request, 'persons/personal-account-settings.html')


@login_required(login_url="login")
def registered_events(request):
    participants = Participant.objects.all().filter(user_owner=request.user).order_by('-created_at')

    # participants = Participant.objects.all()
    # for participant in participants:
    #     if participant.registered_on in list
    # result = {}

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
