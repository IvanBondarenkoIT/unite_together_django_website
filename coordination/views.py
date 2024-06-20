import datetime
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, ParticipantForm, PersonForm
from web_pages.models import Events
from persons.models import Participant, AssociatedPerson

@login_required
# @permission_required('web_pages.view_event', raise_exception=True)
def event_list(request):
    events = Events.objects.all()
    return render(request, 'coordination/event_list.html', {'events': events})

@login_required
# @permission_required('web_pages.add_event', raise_exception=True)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'coordination/event_form.html', {'form': form})

@login_required
# @permission_required('web_pages.change_event', raise_exception=True)
def event_update(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'coordination/event_form.html', {'form': form})

@login_required
# @permission_required('web_pages.delete_event', raise_exception=True)
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'coordination/event_confirm_delete.html', {'object': event})

@login_required
# @permission_required('web_pages.view_participant', raise_exception=True)
def participant_list(request, pk):
    # if pk:
    event = get_object_or_404(Events, pk=pk)
    participants = Participant.objects.all().filter(is_active=True, registered_on=event)
    # else:
    #     participants = Participant.objects.all()

    context = {
        'event': event,
        'participants': participants
    }

    return render(request, 'coordination/participant_list.html', context=context)

@login_required
# @permission_required('web_pages.add_participant', raise_exception=True)
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'coordination/participant_form.html', {'form': form})

@login_required
# @permission_required('web_pages.change_participant', raise_exception=True)
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'coordination/participant_form.html', {'form': form})

@login_required
# @permission_required('web_pages.delete_participant', raise_exception=True)
def participant_delete(request, event_pk, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')

    context = {
        'object': participant,
        'event_pk': event_pk,
    }
    return render(request, 'coordination/participant_confirm_delete.html', context=context)

@login_required
# @permission_required('web_pages.view_person', raise_exception=True)
def person_list(request):
    persons = AssociatedPerson.objects.all()
    return render(request, 'coordination/person_list.html', {'persons': persons})

@login_required
# @permission_required('web_pages.add_person', raise_exception=True)
def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'coordination/person_form.html', {'form': form})

@login_required
# @permission_required('web_pages.change_person', raise_exception=True)
def person_update(request, pk):
    person = get_object_or_404(AssociatedPerson, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)
    return render(request, 'coordination/person_form.html', {'form': form})

@login_required
# @permission_required('web_pages.delete_person', raise_exception=True)
def person_delete(request, pk):
    person = get_object_or_404(AssociatedPerson, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'coordination/person_confirm_delete.html', {'object': person})


def export_participants(request, pk):
    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Participants'

    # Write the headers
    headers = ['Unic ID№', 'Name', 'Email', 'Document', 'Status']  # Adjust headers as needed
    sheet.append(headers)

    # Write data rows
    event = get_object_or_404(Events, pk=pk)
    participants = Participant.objects.all().filter(is_active=True, registered_on=event)

    for participant in participants:
        sheet.append([
            participant.copy_of_unique_identifier,
            f"{participant.first_name}{participant.last_name}",
            participant.user_owner.email,
            participant.document_number,
            participant.status,
            ])  # Adjust fields as needed
    current_datetime = datetime.datetime.now()
    date_string = current_datetime.strftime("%d/%m/%Y")
    # Save the workbook to an HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = f'attachment; filename="participants {event.name} {date_string}.xlsx"'
    response['Content-Disposition'] = f'attachment; filename="participants {date_string}.xlsx"'
    workbook.save(response)

    return response

