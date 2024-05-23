from django.shortcuts import render, redirect

from .forms import PersonForm
from .forms import PersonFormSet
from .models import Person


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
