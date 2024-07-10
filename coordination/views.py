import datetime
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, ParticipantForm, PersonForm
from web_pages.models import Events
from persons.models import Participant, AssociatedPerson, UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
def participant_list(request, pk):
    event = get_object_or_404(Events, pk=pk)

    # Fetch participants for the specific event
    participants = Participant.objects.filter(registered_on=event, is_active=True)

    # Prepare participant details list
    participant_details = []

    for participant in participants:
        try:
            user_profile = UserProfile.objects.get(user=participant.user_owner)
            owner_full_name = user_profile.user.first_name + " " + user_profile.user.last_name
            owner_uid = user_profile.person.unique_identifier
        except UserProfile.DoesNotExist:
            owner_uid = ""
            owner_full_name = ""

        participant_details.append({
            'pk': participant.pk,
            'unique_identifier': participant.copy_of_unique_identifier,
            'full_name': participant.first_name + " " + participant.last_name,
            'date_of_birth': participant.date_of_birth,

            'owner_unique_identifier': owner_uid,
            'owner_full_name': owner_full_name,

            'email': participant.user_owner.email,
            'gender': participant.gender,
            'document': participant.document_number,
            'citizenship': participant.citizenship,
            'city': participant.chosen_city,

            'ge_phone_number': participant.georgian_phone_number,
            'ua_phone_number': participant.ukrainian_phone_number,
        })

    context = {
        'event': event,
        'participants': participant_details,
    }

    return render(request, 'coordination/participant_list.html', context=context)

@login_required
# @permission_required('web_pages.add_participant', raise_exception=True)
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save()
            event_pk = participant.registered_on.pk  # Assuming 'event' is the ForeignKey field in the Participant model
            return redirect('participant_list', pk=event_pk)
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
            participant = form.save()
            event_pk = participant.registered_on.pk  # Assuming 'event' is the ForeignKey field in the Participant model
            return redirect('participant_list', pk=event_pk)
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

    person_details = []

    for person in persons:
        try:
            user_profile = UserProfile.objects.get(user=person.user_owner)
            owner_uid = user_profile.person.unique_identifier
            owner_full_name = user_profile.user.first_name + " " + user_profile.user.last_name
        except UserProfile.DoesNotExist:
            owner_uid = ""
            owner_full_name = ""

        person_details.append({
            'pk': person.pk,
            'unique_identifier': person.unique_identifier,
            'full_name': person.first_name + ' ' + person.last_name,
            'date_of_birth': person.date_of_birth,

            'owner_unique_identifier': owner_uid,
            'owner_full_name': owner_full_name,

            'email': person.user_owner.email,
            # 'status': person.status,  # Assuming status is an attribute of AssociatedPerson
            'gender': person.gender,  # Assuming gender is an attribute of AssociatedPerson
            'document': person.document_number,  # Assuming document is an attribute of AssociatedPerson
            'citizenship': person.citizenship,  # Assuming citizenship is an attribute of AssociatedPerson
            'city': person.chosen_city,  # Assuming city is an attribute of AssociatedPerson
            'ge_phone_number': person.georgian_phone_number,  # Assuming phone_number is an attribute of AssociatedPerson
            'ua_phone_number': person.ukrainian_phone_number,  # Assuming phone_number is an attribute of AssociatedPerson
        })

    return render(request, 'coordination/person_list.html', {'persons': person_details})

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


