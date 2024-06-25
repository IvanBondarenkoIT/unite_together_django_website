from django.shortcuts import render

from web_pages.models import WebContentObject, Events, Projects
from .models import SectionAboutUs, SectionEvents, SectionProjects, CallToAction


def homepage(request):
    sec_about_us = SectionAboutUs.objects.first()
    sec_events = SectionEvents.objects.first()

    sec_projects = SectionProjects.objects.first()
    sec_cta_first = CallToAction.objects.first()
    sec_cta_last = CallToAction.objects.last()

    events_objects = list(Events.objects.filter(show_in_main_page_carousel=True).order_by('order'))
    projects_objects = list(Projects.objects.filter(show_in_main_page_carousel=True).order_by('order'))

    carousel_objects = events_objects + projects_objects

    carousel_objects.sort(key=lambda x: x.order)

    context = {
        'events_objects': events_objects,
        'carousel_objects': carousel_objects,
        'sec_about_us': sec_about_us,
        'sec_events': sec_events,
        'sec_projects': sec_projects,
        'first_cta': sec_cta_first,
        'last_cta': sec_cta_last,
        }
    # print(f"carousel_objects - {carousel_objects}")
    return render(request, 'homepage/index.html', context=context)
    # return render(request, 'homepage/carousel.html', context=context)


# def home(request):
#     # initiatives = Initiative.objects.all().order_by('order')
#     # projects = Projects.objects.all().order_by('order')
#     # events = Events.objects.all().order_by('order')
#
#     context = {
#         'initiatives': initiatives,
#         'projects': projects,
#         'events': events,
#     }
#     return render(request, 'home/index.html', context)