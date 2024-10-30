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
)

OBJECTS_ON_PAGE = 6  # Константа для определения количества объектов на каждой странице


def events(request, group_slug=None):
    """
    Обрабатывает запрос на отображение списка событий, с возможностью фильтрации по
    статусу активности и городу. Поддерживает пагинацию и сохранение фильтров в сессии.
    """
    # Обработка значений чекбокса и выбранного города в зависимости от метода запроса
    if request.method == "POST":
        # Проверка состояния чекбокса и установка значения для фильтра активности
        is_active = request.POST.get("free-spots-checkbox") == "on"
        new_selected_city = request.POST.get("selected-city")

        # Если выбран новый город, сохраняем его в сессии, иначе используем предыдущий выбор
        if new_selected_city:
            selected_city = new_selected_city
            request.session["activeCityFilter"] = selected_city
        else:
            selected_city = request.session.get("activeCityFilter", "All")
            request.session["activeCheckbox"] = is_active
    else:
        # Получаем значения фильтров из сессии для GET-запроса
        is_active = request.session.get("activeCheckbox", False)
        selected_city = request.session.get("activeCityFilter", "All")

    # Создание аргументов фильтрации на основе значения активности
    kw_args = {"is_active": is_active} if is_active else {}

    # Фильтрация по группе событий, если указан `group_slug`
    if group_slug:
        group = get_object_or_404(
            ObjectsGroup, slug=group_slug, page__name__iexact="events", **kw_args
        )
        kw_args["group"] = group

    # Добавление фильтрации по выбранному городу, если он указан
    if selected_city and selected_city != "All":
        _city = get_object_or_404(City, name=selected_city)
        kw_args["selected_city"] = _city

    # Запрос всех событий с указанными фильтрами и добавление аннотации для предварительной генерации URL
    all_objects = (
        Events.objects.filter(**kw_args)
        .select_related("selected_city")
        .annotate(
            pre_computed_url=Concat(
                F("group__slug"), Value("/"), F("slug"), output_field=CharField()
            )
        )
        .order_by("-is_active", "start_date")
    )

    # Пагинация событий
    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)
    objects_count = paginator.count

    # Получение списка городов для выбора в фильтре
    cities = City.objects.only("id", "name").all()

    # Подготовка данных для шаблона
    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
        "cities": cities,
        "selected_city": selected_city,
    }

    return render(request, "events/events_index.html", context=context)


def create_participant(
    selected_associated_person: AssociatedPerson, selected_event: WebContentObject
) -> Participant:
    """
    Создает нового участника мероприятия из данных существующего связанного лица и события.

    Args:
        selected_associated_person (AssociatedPerson): Связанное лицо, которое будет скопировано.
        selected_event (WebContentObject): Мероприятие, с которым будет связан новый участник.

    Returns:
        Participant: Созданный экземпляр участника.
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


def event_detail(request, group_slug=None, event_slug=None):
    """
    Отображает детальную информацию о событии, с возможностью регистрации связанного лица
    как участника на событие, при условии авторизации пользователя.
    """
    try:
        single_event = Events.objects.select_related("group").get(
            group__slug=group_slug, slug=event_slug
        )
    except Events.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect("some_error_page")  # Замените на свою страницу с ошибкой

    # Если пользователь аутентифицирован, получаем список доступных для выбора лиц
    if request.user.is_authenticated:
        persons = AssociatedPerson.objects.filter(
            user_owner=request.user, is_approved=True
        ).order_by("unique_identifier")

        # Обработка POST-запроса при регистрации лиц на мероприятие
        if request.method == "POST":
            selected_person_ids = request.POST.getlist("selected-persons")
            if selected_person_ids:
                for person_id in selected_person_ids:
                    try:
                        selected_person = AssociatedPerson.objects.get(
                            id=person_id, user_owner=request.user
                        )
                        total_participants_in_event = Participant.objects.filter(
                            registered_on=single_event
                        ).count()
                        # Проверка доступных мест и добавление участника
                        if single_event.max_participants > total_participants_in_event:
                            if not Participant.objects.filter(
                                copy_of_unique_identifier=selected_person.unique_identifier,
                                registered_on=single_event,
                            ).exists():
                                create_participant(selected_person, single_event)
                                messages.success(
                                    request,
                                    f"Person {selected_person.first_name} {selected_person.last_name} registered for {single_event.name}",
                                )
                            else:
                                messages.warning(
                                    request,
                                    f"Person {selected_person.first_name} {selected_person.last_name} is already registered for this event.",
                                )
                        else:
                            messages.error(
                                request,
                                f"Person {selected_person.first_name} {selected_person.last_name} is not registered. Maximum number of participants has been reached!",
                            )
                            single_event.is_active = False
                            single_event.save()
                            break
                    except AssociatedPerson.DoesNotExist:
                        messages.error(
                            request, "Person not found or not owned by the user."
                        )
                return redirect("registered_events")
    else:
        persons = []

    context = {
        "single_event": single_event,
        "persons": persons,
    }

    return render(request, "events/event_detail.html", context=context)


def projects(request, group_slug=None):
    """
    Обрабатывает запрос на отображение списка проектов, с возможностью фильтрации
    по активности и пагинацией, с сохранением состояния чекбокса в сессии.
    """
    # Обработка значений чекбокса для фильтрации по активности проектов
    if request.method == "POST":
        is_active = request.POST.get("free-spots-checkbox") == "on"
        request.session["activeCheckbox"] = is_active
    else:
        is_active = request.session.get("activeCheckbox", False)

    # Подготовка словаря фильтров
    kw_args = {"is_active": is_active} if is_active else {}

    # Фильтрация по группе проектов, если указан `group_slug`
    if group_slug:
        group = get_object_or_404(
            ObjectsGroup, slug=group_slug, page__name__iexact="projects", **kw_args
        )
        kw_args["group"] = group

    # Получение всех проектов с указанными фильтрами и применением пагинации
    all_objects = Projects.objects.filter(**kw_args).select_related("group__page")

    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)
    objects_count = paginator.count

    # Подготовка данных для шаблона
    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
    }

    return render(request, "projects/projects.html", context=context)


def projects_detail(request, group_slug=None, project_slug=None):
    """
    Отображает детальную информацию о проекте, включая галерею, если она имеется.
    """
    single_project = get_object_or_404(
        Projects, group__slug=group_slug, slug=project_slug
    )
    project_gallery = ProjectGallery.objects.filter(project_id=single_project.id)

    context = {
        "single_project": single_project,
        "project_gallery": project_gallery,
    }

    return render(request, "projects/project-detail.html", context=context)
