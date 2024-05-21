from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import PersonForm


def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Change to your desired redirect target
    else:
        form = PersonForm()

    return render(request, 'persons/create_person.html', {'form': form})
