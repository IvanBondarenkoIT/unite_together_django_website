from django.shortcuts import render

from web_pages.models import WebContentObject
from .models import SectionAboutUs, SectionEvents, SectionProjects


def homepage(request):
    about_us = SectionAboutUs.objects.all()
    events = SectionEvents.objects.all()
    projects = SectionProjects.objects.all()

    carousel_objects = WebContentObject.objects.filter(show_in_main_page_carousel=True).order_by('order')

    context = {
        'carousel_objects': carousel_objects,
        'about_us': about_us,
        'events': events,
        'projects': projects
        }
    # print(f"carousel_objects - {carousel_objects}")
    # return render(request, 'homepage/index.html', context=context)
    return render(request, 'homepage/carousel.html', context=context)


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