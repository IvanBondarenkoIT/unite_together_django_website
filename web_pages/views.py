from django.shortcuts import render

from web_pages.models import WebPage, WebContentObject, WebContentSubordinateObject


def home(request):
    return render(request, "events/events_index.html")


def about_us(request):
    try:
        stats_section = WebContentObject.objects.get(name="about_us_stats")
        stats_section_subs = WebContentSubordinateObject.objects.all().filter(content_master_object=stats_section)


        context = {
            "header": WebContentObject.objects.get(name="about_us_header"),
            "mission": WebContentObject.objects.get(name="about_us_mission"),
            "stats": stats_section,
            "stats_subs": stats_section_subs,
            "history": stats_section,
            "history_subs": stats_section_subs,
            "achievements": stats_section,
            "achievements_subs": stats_section_subs,

        }
    except WebContentObject:
        context = {}

    return render(request, 'about_us.html', context=context)


def events(request):
    try:
        # stats_section = WebContentObject.objects.get(name="about_us_stats")
        # stats_section_subs = WebContentSubordinateObject.objects.all().filter(content_master_object=stats_section)
        #
        #
        #
        #
        # context = {
        #     "header": WebContentObject.objects.get(name="about_us_header"),
        #     "mission": WebContentObject.objects.get(name="about_us_mission"),
        #     "stats": stats_section,
        #     "stats_subs": stats_section_subs,
        #     "history": stats_section,
        #     "history_subs": stats_section_subs,
        #     "achievements": stats_section,
        #     "achievements_subs": stats_section_subs,
        #
        # }

        all_objects = WebContentObject.objects.all()
        print(f"all_objects {list(all_objects)}")
        context = {
            "all_objects": all_objects,
        }

    except WebContentObject:
        context = {}

    return render(request, 'events/events_index.html', context=context)
