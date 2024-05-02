from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from web_pages.models import WebPage, WebContentObject, WebContentSubordinateObject, Events, ObjectsGroup


def home(request):
    return render(request, "base.html")


def about_us(request):
    # try:
    #     stats_section = WebContentObject.objects.get(name="about_us_stats")
    #     stats_section_subs = WebContentSubordinateObject.objects.all().filter(content_master_object=stats_section)
    #
    #     context = {
    #         # "header": WebContentObject.objects.get(name="about_us_header"),
    #         # "mission": WebContentObject.objects.get(name="about_us_mission"),
    #         "header": stats_section,
    #         "stats": stats_section,
    #         "stats_subs": stats_section_subs,
    #         "history": stats_section,
    #         "history_subs": stats_section_subs,
    #         "achievements": stats_section,
    #         "achievements_subs": stats_section_subs,
    #
    #     }
    # except WebContentObject:
    context = {}

    return render(request, 'aboutus/aboutus_index.html', context=context)


def events(request, group_slug=None):

    if request.method == 'GET':

        # Get the checkbox state from the session, default to False if not set
        is_active = request.session.get('activeCheckbox', False)
        print(f"GET {is_active}")

        if group_slug:
            group = get_object_or_404(ObjectsGroup, slug=group_slug)
            if is_active:
                all_objects = Events.objects.filter(group=group, is_active=True)
            else:
                all_objects = Events.objects.all().filter().order_by("id")
        else:
            if is_active:
                all_objects = Events.objects.all().filter(is_active=True).order_by("id")
            else:
                all_objects = Events.objects.all().filter().order_by("id")
    elif request.method == 'POST':

        # Save the checkbox state to the session
        is_active = request.POST.get('activeCheckbox', False)
        print(f"POST{is_active}")
        request.session['activeCheckbox'] = is_active == 'on'
        return redirect('your_view')

    paginator = Paginator(all_objects, 2)
    page = request.GET.get("page")
    page_all_objects = paginator.get_page(page)

    objects_count = all_objects.count()

    context = {
        "all_objects": page_all_objects,
        "objects_count": objects_count,
        "free_spots": is_active,
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
    context = {}
    return render(request, 'projects/projects_index.html', context=context)
