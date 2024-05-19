from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from web_pages.models import WebPage, WebContentObject, WebContentSubordinateObject, Events, ObjectsGroup, City, \
    Projects

OBJECTS_ON_PAGE = 6


def home(request):
    return render(request, "home/index.html")


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
        group = get_object_or_404(ObjectsGroup, slug=group_slug)
        kw_args["group"] = group

    if selected_city and selected_city != "All":  # If city option selected "All" then no filter by city
        _city = get_object_or_404(City, name=selected_city)
        kw_args['selected_city'] = _city

    all_objects = Events.objects.all().filter(**kw_args).order_by("id")

    # Pagination functional
    paginator = Paginator(all_objects, OBJECTS_ON_PAGE)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)

    objects_count = all_objects.count()

    cities = City.objects.all()

    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
        "cities": cities,
        "selected_city": selected_city,
    }

    return render(request, 'events/events_index.html', context=context)


def event_detail(request, group_slug=None, event_slug=None):
    try:
        single_event = Events.objects.get(group__slug=group_slug, slug=event_slug)
    except Exception as error:
        raise error

        # event = get_object_or_404(Events, slug=event_slug)

    context = {
        "single_event": single_event,
    }

    return render(request, 'events/event_detail.html', context=context)


def projects(request, group_slug=None):
    all_objects = Projects.objects.all().filter().order_by("id")
    context = {"all_objects": all_objects,}
    return render(request, 'projects/projects.html', context=context)


def projects_detail(request, group_slug=None, project_slug=None):
    context = {}
    return render(request, 'projects/project-detail.html', context=context)


def about_us(request):
    context = {}
    return render(request, 'aboutus/aboutus_index.html', context=context)


def history(request):
    context = {}
    return render(request, 'aboutus/about-us-history.html', context=context)


def documents(request):
    context = {}
    return render(request, 'aboutus/about-us-documents.html', context=context)


def partners(request):
    context = {}
    return render(request, 'aboutus/about-us-partners.html', context=context)


def contacts(request):
    context = {}
    return render(request, 'aboutus/about-us-contacts.html')
