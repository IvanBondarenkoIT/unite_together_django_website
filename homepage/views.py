from django.shortcuts import render

from web_pages.models import WebContentObject
from .models import SectionAboutUs, SectionEvents, SectionProjects, CallToAction


def homepage(request):
    sec_about_us = SectionAboutUs.objects.first()
    sec_events = SectionEvents.objects.first()
    sec_projects = SectionProjects.objects.first()
    sec_cta_first = CallToAction.objects.first()
    sec_cta_last = CallToAction.objects.last()

    carousel_objects = WebContentObject.objects.filter(show_in_main_page_carousel=True).order_by('order')

    context = {
        'carousel_objects': carousel_objects,
        'about_us': sec_about_us,
        'events': sec_events,
        'projects': sec_projects
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