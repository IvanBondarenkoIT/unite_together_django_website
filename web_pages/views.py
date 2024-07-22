from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import F, CharField, Value
from django.db.models.functions import Concat

from persons.models import AssociatedPerson, Participant
from web_pages.models import WebContentObject, Events, ObjectsGroup, City, Projects, ProjectGallery

OBJECTS_ON_PAGE = 6


def events(request, group_slug=None):
    if request.method == 'GET':
        # Get the checkbox state from the session, default to False if not set
        is_active = request.session.get('activeCheckbox', False)
        selected_city = request.session.get('activeCityFilter', "All")

    elif request.method == 'POST':
        # Save the selected City state to the session
        new_selected_city = request.POST.get("selected-city")

        if new_selected_city is None:  # It means that POST not from City selector
            selected_city = request.session.get('activeCityFilter', "All")  # Get old value from session or default All

            is_active = request.POST.get("free-spots-checkbox") == "on"  # It means checkbox change to True or False
            request.session['activeCheckbox'] = is_active

        else:
            selected_city = new_selected_city
            request.session['activeCityFilter'] = new_selected_city
            is_active = request.session.get('activeCheckbox', False)  # Checkbox stay with old value
    else:
        is_active = request.session.get('activeCheckbox', False)
        selected_city = request.session.get('activeCityFilter', "All")

    kw_args = {}

    if is_active:
        kw_args = {"is_active": is_active}

    if group_slug:  # If have group_slug - added filter by group
        group = get_object_or_404(ObjectsGroup, slug=group_slug, page__name__iexact='events', **kw_args)
        kw_args["group"] = group

    if selected_city and selected_city != "All":  # If city option selected "All" then no filter by city
        _city = get_object_or_404(City, name=selected_city)
        kw_args['selected_city'] = _city

    #     all_objects = Events.objects.all().filter(**kw_args).order_by("id")

    # Pilippio update
    all_objects = Events.objects.filter(**kw_args).select_related('selected_city').annotate(
        pre_computed_url=Concat(F('group__slug'), Value('/'), F('slug'), output_field=CharField())
    ).order_by("-is_active", "start_date")
    # all_objects = Events.objects.all().filter(**kw_args).order_by("id").select_related('group__page')

    # Pagination functional
    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)

    # Get count efficiently / faster
    objects_count = paginator.count

    # Optimize fetching cities if related to events
    cities = City.objects.only('id', 'name').all()

    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
        "cities": cities,
        "selected_city": selected_city,
    }

    # print(request.path)
    return render(request, 'events/events_index.html', context=context)


def create_participant(selected_associated_person: AssociatedPerson, selected_event: WebContentObject) -> Participant:
    """
    Create a new Participant from an AssociatedPerson and a WebContentObject (event).

    Args:
        selected_associated_person (AssociatedPerson): The associated person to be copied.
        selected_event (WebContentObject): The event to associate with the new participant.

    Returns:
        Participant: The created Participant instance.
    """
    new_participant = Participant.objects.create(
        user_owner=selected_associated_person.user_owner,
        first_name=selected_associated_person.first_name,
        last_name=selected_associated_person.last_name,
        date_of_birth=selected_associated_person.date_of_birth,
        citizenship=selected_associated_person.citizenship,
        date_of_arrival=selected_associated_person.date_of_arrival,
        type_of_document=selected_associated_person.type_of_document,
        document_number=selected_associated_person.document_number,
        gender=selected_associated_person.gender,
        georgian_phone_number=selected_associated_person.georgian_phone_number,
        ukrainian_phone_number=selected_associated_person.ukrainian_phone_number,
        country=selected_associated_person.country,
        chosen_city=selected_associated_person.chosen_city,
        address_line=selected_associated_person.address_line,
        is_active=selected_associated_person.is_active,
        copy_of_unique_identifier=selected_associated_person.unique_identifier,

        status="Registered",
        registered_on=selected_event,

    )
    return new_participant


def event_detail(request, group_slug=None, event_slug=None):
    try:
        single_event = Events.objects.select_related('group').get(group__slug=group_slug, slug=event_slug)
    except Events.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('some_error_page')  # Replace with your error handling page

    if request.user.is_authenticated:
        persons = AssociatedPerson.objects.filter(user_owner=request.user, is_approved=True).order_by('unique_identifier')

        if request.method == "POST":
            selected_person_ids = request.POST.getlist('selected-persons')
            if selected_person_ids:
                for person_id in selected_person_ids:
                    try:
                        selected_person = AssociatedPerson.objects.get(id=person_id, user_owner=request.user)
                        total_participants_in_event = Participant.objects.filter(registered_on=single_event).count()
                        if single_event.max_participants > total_participants_in_event:
                            if not Participant.objects.filter(person=selected_person, registered_on=single_event).exists():
                                new_participant = create_participant(selected_person, single_event)
                                messages.success(request, f"Person {new_participant.first_name} {new_participant.last_name} registered for {single_event.name}")
                            else:
                                messages.warning(request, f"Person {selected_person.first_name} {selected_person.last_name} is already registered for this event.")
                        else:
                            messages.error(request, f"Person {selected_person.first_name} {selected_person.last_name} is not registered. Maximum number of participants has been reached!")
                            single_event.is_active = False
                            single_event.save()
                            break
                    except AssociatedPerson.DoesNotExist:
                        messages.error(request, "Person not found or not owned by the user.")
                return redirect('registered_events')

    else:
        persons = []

    context = {
        "single_event": single_event,
        "persons": persons,
    }

    return render(request, 'events/event_detail.html', context=context)



def projects(request, group_slug=None):

    if request.method == 'POST':
        is_active = request.POST.get("free-spots-checkbox") == "on"  # It means checkbox change to True or False
        request.session['activeCheckbox'] = is_active
    else:
        is_active = request.session.get('activeCheckbox', False)

    kw_args = {}

    if is_active:
        kw_args = {"is_active": is_active}

    if group_slug:  # If have group_slug - added filter by group
        group = get_object_or_404(ObjectsGroup, slug=group_slug, page__name__iexact='projects', **kw_args)
        kw_args["group"] = group

    # this is a sample how to speedify x3 sql query
    all_objects = Projects.objects.all().filter(**kw_args).select_related('group__page')

    # all_objects = Projects.objects.filter(**kw_args).select_related('selected_city').annotate(
    #     pre_computed_url=Concat(F('group__slug'), Value('/'), F('slug'), output_field=CharField())
    # ).order_by("id")

    # Pagination functional
    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)
    # Get count efficiently / faster
    objects_count = paginator.count

    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
    }

    return render(request, 'projects/projects.html', context=context)


def projects_detail(request, group_slug=None, project_slug=None):
    try:
        single_project = Projects.objects.get(group__slug=group_slug, slug=project_slug)
    except Exception as error:
        raise error

        # event = get_object_or_404(Events, slug=event_slug)

    project_gallery = ProjectGallery.objects.filter(project_id=single_project.id)

    context = {
        "single_project": single_project,
        "project_gallery": project_gallery,
    }

    return render(request, 'projects/project-detail.html', context=context)

