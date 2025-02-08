from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, CharField, Value
from django.db.models.functions import Concat
from persons.models import AssociatedPerson, Participant

from web_pages.models import (
    WebContentObject,
    Events,
    ObjectsGroup,
    City,
    Projects,
    ProjectGallery,
    BannerSettings,
)

from django.core.mail import send_mail
from django.http import HttpResponse

OBJECTS_ON_PAGE = 6  # Constant defining the number of objects per page


def get_banner_settings():
    settings, created = BannerSettings.objects.get_or_create(
        id=1
    )  # id=1 для уникальности
    return settings


def events(request, group_slug=None, lang="uk"):
    """
    Renders a paginated list of events with optional filtering by city and activity status.
    Saves filter selections in the session for consistent user experience.

    Args:
        request: The HTTP request object.
        group_slug (str, optional): Slug of the events group for filtering.

    Returns:
        HttpResponse: Rendered template for the list of events.
    """
    print(f"Lang:{lang}")
    # Process checkbox and city selection based on the request method
    if request.method == "POST":
        # Determine checkbox status for filtering active events
        is_active = request.POST.get("free-spots-checkbox") == "on"
        new_selected_city = request.POST.get("selected-city")

        # Update session with new city if selected; otherwise, use previous selection
        if new_selected_city:
            selected_city = new_selected_city
            request.session["activeCityFilter"] = selected_city
        else:
            selected_city = request.session.get("activeCityFilter", "All")
            request.session["activeCheckbox"] = is_active
    else:
        # Get filter values from session for GET requests
        is_active = request.session.get("activeCheckbox", False)
        selected_city = request.session.get("activeCityFilter", "All")

    # Build filter arguments based on activity status
    kw_args = {"is_active": is_active} if is_active else {}

    # Filter by event group if specified
    if group_slug:
        group = get_object_or_404(
            ObjectsGroup, slug=group_slug, page__name__iexact="events", **kw_args
        )
        kw_args["group"] = group

    # Add city filter if a specific city is selected
    if selected_city and selected_city != "All":
        _city = get_object_or_404(City, name=selected_city)
        kw_args["selected_city"] = _city

    # Not archived objects
    kw_args["is_archived"] = False

    # Retrieve events matching filters and annotate with precomputed URLs
    all_objects = (
        Events.objects.filter(**kw_args)
        .select_related("selected_city")
        .annotate(
            pre_computed_url=Concat(
                F("group__slug"), Value("/"), F("slug"), output_field=CharField()
            )
        )
        .order_by("-is_active", "-start_date")
    )

    # Paginate events
    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)
    objects_count = paginator.count

    # Retrieve list of cities for filter selection
    cities = City.objects.only("id", "name").all()
    banner_settings = BannerSettings.objects.first()

    # Prepare context data for the template
    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
        "cities": cities,
        "selected_city": selected_city,
        "banner_settings": banner_settings,
    }

    return render(request, "events/events_index.html", context=context)


def create_participant(
    selected_associated_person: AssociatedPerson, selected_event: WebContentObject
) -> Participant:
    """
    Creates a new event participant based on an existing associated person and links them to the event.

    Args:
        selected_associated_person (AssociatedPerson): The associated person data.
        selected_event (WebContentObject): The event for which the participant is registered.

    Returns:
        Participant: The created participant instance.
    """
    return Participant.objects.create(
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


def event_detail(request, group_slug=None, event_slug=None, lang="uk"):
    """
    Відображає детальну інформацію про конкретну подію з можливістю реєстрації для авторизованих користувачів.

    Аргументи:
        request: Об'єкт HTTP запиту.
        group_slug (str, optional): Слаг групи події.
        event_slug (str, optional): Слаг події.

    Повертає:
        HttpResponse: Відрендерений шаблон для сторінки деталей події.
    """
    try:
        single_event = Events.objects.select_related("group").get(
            group__slug=group_slug, slug=event_slug
        )
    except Events.DoesNotExist:
        messages.error(request, "Подію не знайдено.")
        return redirect("some_error_page")  # Замініть на вашу сторінку помилки

    # Якщо користувач авторизований, отримати список затверджених осіб
    if request.user.is_authenticated:
        persons = AssociatedPerson.objects.filter(
            user_owner=request.user,
            is_approved=True,
        ).order_by("unique_identifier")

        # Сохраняем данные в сессию
        request.session["last_event"] = {
            "url": request.path,
            "name": single_event.name,
            "thumbnail": (single_event.image.url if single_event.image else None),
        }

        # Обробка POST запиту для реєстрації на подію
        if request.method == "POST":
            selected_person_ids = request.POST.getlist("selected-persons")
            if selected_person_ids:
                for person_id in selected_person_ids:
                    try:
                        selected_person = AssociatedPerson.objects.get(
                            id=person_id, user_owner=request.user
                        )
                        # Перевірка віку
                        if (
                            single_event.end_age
                            >= selected_person.get_current_age()
                            >= single_event.start_age
                        ):

                            total_participants_in_event = Participant.objects.filter(
                                registered_on=single_event
                            ).count()
                            # Перевірити наявність місць та додати учасника
                            if (
                                single_event.max_participants
                                >= total_participants_in_event
                            ):
                                if not Participant.objects.filter(
                                    copy_of_unique_identifier=selected_person.unique_identifier,
                                    registered_on=single_event,
                                ).exists():
                                    create_participant(selected_person, single_event)
                                    messages.success(
                                        request,
                                        f"Особа {selected_person.first_name} {selected_person.last_name} зареєстрована на {single_event.name}",
                                    )
                                else:
                                    messages.warning(
                                        request,
                                        f"Особа {selected_person.first_name} {selected_person.last_name} вже зареєстрована на цю подію.",
                                    )
                            else:
                                messages.error(
                                    request,
                                    f"Особа {selected_person.first_name} {selected_person.last_name} не зареєстрована. Досягнуто максимальну кількість учасників!",
                                )
                                single_event.is_active = False
                                single_event.save()
                                break
                        else:
                            messages.error(
                                request,
                                f"Особа {selected_person.first_name} {selected_person.last_name} не зареєстрована. Критерії віку не відповідають!",
                            )
                    except AssociatedPerson.DoesNotExist:
                        messages.error(
                            request,
                            "Особу не знайдено або вона не належить користувачу.",
                        )
                return redirect("registered_events")
    else:
        persons = []

    context = {
        "single_event": single_event,
        "persons": persons,
    }

    return render(request, "events/event_detail.html", context=context)


def projects(request, group_slug=None, lang="uk"):
    """
    Renders a paginated list of projects with an option to filter by activity status, saving filter state in session.

    Args:
        request: The HTTP request object.
        group_slug (str, optional): Slug of the projects group.

    Returns:
        HttpResponse: Rendered template for the list of projects.
    """
    print(f"Lang:{lang}")
    if request.method == "POST":
        is_active = request.POST.get("free-spots-checkbox") == "on"
        request.session["activeCheckbox"] = is_active
    else:
        is_active = request.session.get("activeCheckbox", False)

    kw_args = {"is_active": is_active} if is_active else {}

    if group_slug:
        group = get_object_or_404(
            ObjectsGroup, slug=group_slug, page__name__iexact="projects", **kw_args
        )
        kw_args["group"] = group

    # Not archived objects
    kw_args["is_archived"] = False

    all_objects = (
        Projects.objects.filter(**kw_args)
        .select_related("group__page")
        .order_by("-is_active", "-order")
    )

    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)
    objects_count = paginator.count

    banner_settings = BannerSettings.objects.first()

    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
        "banner_settings": banner_settings,
        "lang": lang,
    }

    return render(request, "projects/projects.html", context=context)


def projects_detail(request, group_slug=None, project_slug=None, lang="uk"):
    """
    Displays detailed information about a specific project, including a gallery if available.

    Args:
        request: The HTTP request object.
        group_slug (str, optional): Slug of the project group.
        project_slug (str, optional): Slug of the project.

    Returns:
        HttpResponse: Rendered template for the project detail page.
    """
    print(f"Lang:{lang}")
    single_project = get_object_or_404(
        Projects, group__slug=group_slug, slug=project_slug
    )
    project_gallery = ProjectGallery.objects.filter(project_id=single_project.id)

    all_cities = single_project.selected_cities_list.all()
    banner_settings = BannerSettings.objects.first()

    context = {
        "single_project": single_project,
        "project_gallery": project_gallery,
        "cities": all_cities,
        "banner_settings": banner_settings,
        "lang": lang,
    }

    return render(request, "projects/project-detail.html", context=context)


def test_email_view(request):
    subject = "Тестовое письмо"
    message = "Привет! Это тестовое письмо для проверки SMTP-конфигурации."
    from_email = "info@unite-together.org"
    recipient_list = ["krenkroyt@gmail.com"]  # Замените на ваш email для тестирования

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Письмо успешно отправлено!")
    except Exception as e:
        return HttpResponse(f"Ошибка при отправке письма: {e}")
