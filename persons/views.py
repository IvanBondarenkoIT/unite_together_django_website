from django.shortcuts import render, redirect

from .forms import PersonForm, ParticipantForm
from .forms import PersonFormSet, ParticipantFormSet

from .models import Person, Participant


def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Change to your desired redirect target
    else:
        form = PersonForm()

    return render(request, 'persons/create_person.html', {'form': form})


def person_list(request):
    if request.method == 'POST':
        formset = PersonFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('person_list')  # Change to your desired redirect target
    else:
        formset = PersonFormSet(queryset=Person.objects.all())

    return render(request, 'persons/person_list.html', {'formset': formset})


def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')  # Change to your desired redirect target
    else:
        form = ParticipantForm()

    return render(request, 'persons/create_participant.html', {'form': form})


def participant_list(request):
    if request.method == 'POST':
        formset = ParticipantFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('participant_list')  # Change to your desired redirect target
    else:
        formset = ParticipantFormSet(queryset=Participant.objects.all())

    return render(request, 'persons/participant_list.html', {'formset': formset})