import datetime
import openpyxl
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, ParticipantForm, AssociatedPersonForm
from web_pages.models import Events
from persons.models import Participant, AssociatedPerson, UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponseForbidden
from functools import wraps


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return _wrapped_view


def supervisor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_supervisor:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")

    return _wrapped_view


@login_required
@staff_required
# @permission_required('web_pages.view_event', raise_exception=True)
def event_list(request):
    events = Events.objects.all().order_by("-updated_at")
    return render(request, "coordination/event_list.html", {"events": events})


@login_required
@staff_required
@supervisor_required
# @permission_required('web_pages.add_event', raise_exception=True)
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created")
            return redirect("event_list")
    else:
        form = EventForm()

    return render(request, "coordination/event_form.html", {"form": form})


@login_required
@staff_required
@supervisor_required
# @permission_required('web_pages.change_event', raise_exception=True)
def event_update(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated")
            return redirect("event_list")
        else:
            # Extract and format errors from the form
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            formatted_errors = " ".join(error_messages)
            messages.error(request, f"Event update failed!\n {formatted_errors}")
    else:
        form = EventForm(instance=event)
    return render(request, "coordination/event_form.html", {"form": form})


@login_required
@staff_required
@supervisor_required
# @permission_required('web_pages.delete_event', raise_exception=True)
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted")
        return redirect("event_list")
    return render(request, "coordination/event_confirm_delete.html", {"object": event})


@login_required
@staff_required
def participant_list(request, pk):
    event = get_object_or_404(Events, pk=pk)

    # Fetch participants for the specific event
    participants = Participant.objects.filter(registered_on=event, is_active=True)

    # Prepare participant details list
    participant_details = []

    for participant in participants:
        try:
            user_profile = UserProfile.objects.get(user=participant.user_owner)
            owner_full_name = (
                user_profile.user.first_name + " " + user_profile.user.last_name
            )
            owner_uid = user_profile.person.unique_identifier
        except UserProfile.DoesNotExist:
            owner_uid = ""
            owner_full_name = ""

        participant_details.append(
            {
                "pk": participant.pk,
                "unique_identifier": participant.copy_of_unique_identifier,
                "full_name": str(participant.first_name)
                + " "
                + str(participant.last_name),
                "date_of_birth": participant.date_of_birth,
                "owner_unique_identifier": owner_uid,
                "owner_full_name": owner_full_name,
                "email": participant.user_owner.email,
                "gender": participant.gender,
                "document": participant.document_number,
                "citizenship": participant.citizenship,
                "city": participant.chosen_city,
                "status": participant.status,
                "registered_at": participant.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "ge_phone_number": participant.georgian_phone_number,
                "ua_phone_number": participant.ukrainian_phone_number,
            }
        )

    context = {
        "event": event,
        "participants": participant_details,
    }

    return render(request, "coordination/participant_list.html", context=context)


@login_required
@staff_required
# @permission_required('web_pages.add_participant', raise_exception=True)
def participant_create(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save()
            event_pk = (
                participant.registered_on.pk
            )  # Assuming 'event' is the ForeignKey field in the Participant model

            messages.success(request, "Participant created successfully!")
            return redirect("participant_list", pk=event_pk)
        else:
            # Extract and format errors from the form
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            formatted_errors = " ".join(error_messages)
            messages.error(request, f"Participant create failed!\n {formatted_errors}")
    else:
        form = ParticipantForm()
    return render(request, "coordination/participant_form.html", {"form": form})


@login_required
@staff_required
# @permission_required('web_pages.change_participant', raise_exception=True)
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        form = ParticipantForm(request.POST, request.FILES, instance=participant)
        if form.is_valid():
            participant = form.save()
            event_pk = (
                participant.registered_on.pk
            )  # Assuming 'event' is the ForeignKey field in the Participant model
            messages.success(request, "Participant updated successfully!")
            return redirect("participant_list", pk=event_pk)
        else:
            # Extract and format errors from the form
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            formatted_errors = " ".join(error_messages)
            messages.error(request, f"Participant update failed!\n {formatted_errors}")
    else:
        form = ParticipantForm(instance=participant)
    return render(request, "coordination/participant_form.html", {"form": form})


@login_required
@staff_required
# @permission_required('web_pages.delete_participant', raise_exception=True)
def participant_delete(request, event_pk, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully")
        return redirect("participant_list", pk=event_pk)

    context = {
        "object": participant,
        "event_pk": event_pk,
    }
    return render(
        request, "coordination/participant_confirm_delete.html", context=context
    )


@login_required
@supervisor_required
# @permission_required('web_pages.view_person', raise_exception=True)
def person_list(request):
    persons = AssociatedPerson.objects.all()

    person_details = []

    for person in persons:
        try:
            user_profile = UserProfile.objects.get(user=person.user_owner)
            owner_uid = user_profile.person.unique_identifier
            owner_full_name = (
                str(user_profile.user.first_name)
                + " "
                + str(user_profile.user.last_name)
            )
        except UserProfile.DoesNotExist:
            owner_uid = ""
            owner_full_name = ""

        person_details.append(
            {
                "pk": person.pk,
                "unique_identifier": person.unique_identifier,
                "full_name": str(person.first_name) + " " + str(person.last_name),
                "date_of_birth": person.date_of_birth,
                "owner_unique_identifier": owner_uid,
                "owner_full_name": owner_full_name,
                "email": person.user_owner.email,
                # 'status': person.status,  # Assuming status is an attribute of AssociatedPerson
                "gender": person.gender,  # Assuming gender is an attribute of AssociatedPerson
                "document": person.document_number,  # Assuming document is an attribute of AssociatedPerson
                "citizenship": person.citizenship,  # Assuming citizenship is an attribute of AssociatedPerson
                "city": person.chosen_city,  # Assuming city is an attribute of AssociatedPerson
                "ge_phone_number": person.georgian_phone_number,
                # Assuming phone_number is an attribute of AssociatedPerson
                "ua_phone_number": person.ukrainian_phone_number,
                # Assuming phone_number is an attribute of AssociatedPerson
            }
        )

    return render(request, "coordination/person_list.html", {"persons": person_details})


@login_required
@supervisor_required
# @permission_required('web_pages.add_person', raise_exception=True)
def person_create(request, lang="uk"):
    if request.method == "POST":
        form = AssociatedPersonForm(request.POST, request.FILES, lang=lang)
        if form.is_valid():
            form.save()
            messages.success(request, "Person created successfully!")
            return redirect("person_list")

    else:
        form = AssociatedPersonForm(lang=lang)
    return render(request, "coordination/person_form.html", {"form": form})


@login_required
@supervisor_required
# @permission_required('web_pages.change_person', raise_exception=True)
def person_update(request, pk, lang="uk"):
    person = get_object_or_404(AssociatedPerson, pk=pk)
    if request.method == "POST":
        form = AssociatedPersonForm(
            request.POST, request.FILES, instance=person, lang=lang
        )
        if form.is_valid():
            messages.success(request, "Person updated successfully!")
            form.save()
            return redirect("coordination_person_list")
        else:
            # Extract and format errors from the form
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            formatted_errors = " ".join(error_messages)
            messages.error(request, f"Person update failed!\n {formatted_errors}")
    else:
        form = AssociatedPersonForm(instance=person, lang=lang)
    return render(request, "coordination/person_form.html", {"form": form})


@login_required
@supervisor_required
# @permission_required('web_pages.delete_person', raise_exception=True)
def person_delete(request, pk):

    person = get_object_or_404(AssociatedPerson, pk=pk)
    if request.method == "POST":
        person.delete()
        return redirect("person_list")
    return render(
        request, "coordination/person_confirm_delete.html", {"object": person}
    )


@login_required
@staff_required
def export_participants(request, pk):
    if request.user.is_staff:
        # Create a workbook and add a worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Participants"

        # Write the headers
        headers = [
            "Unic ID",
            "Participant Name",
            "Email",
            "Document",
            "Status",
            "Birth Date",
            "User UID",
            "User Full Name",
            "User GE phone №",
            "User UA phone №",
        ]  # Adjust headers as needed
        sheet.append(headers)

        # Write data rows
        event = get_object_or_404(Events, pk=pk)
        participants = Participant.objects.all().filter(
            is_active=True, registered_on=event
        )

        for participant in participants:
            sheet.append(
                [
                    participant.copy_of_unique_identifier,
                    f"{participant.first_name} {participant.last_name}",
                    participant.user_owner.email,
                    participant.document_number,
                    participant.status,
                    participant.date_of_birth,
                    participant.user_owner.associated_person.unique_identifier,
                    f"{participant.user_owner.associated_person.first_name} {participant.user_owner.associated_person.last_name}",
                    participant.user_owner.associated_person.georgian_phone_number,
                    participant.user_owner.associated_person.ukrainian_phone_number,
                ]
            )  # Adjust fields as needed
        current_datetime = datetime.datetime.now()
        date_string = current_datetime.strftime("%d/%m/%Y")
        # Save the workbook to an HttpResponse
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # response['Content-Disposition'] = f'attachment; filename="participants {event.name} {date_string}.xlsx"'
        response["Content-Disposition"] = (
            f'attachment; filename="participants {date_string}.xlsx"'
        )
        workbook.save(response)

        return response
    else:
        return redirect("home")
