import os
from django.conf import settings
from django.shortcuts import render, redirect

from web_pages.models import WebContentObject, Events, Projects
from .models import SectionAboutUs, SectionEvents, SectionProjects, CallToAction


from django.views.generic.base import RedirectView


class HomeRedirectView(RedirectView):
    permanent = True  # Если False, то будет 302 вместо 301

    def get_redirect_url(self, *args, **kwargs):
        return self.request.build_absolute_uri(f"/en/homepage/")  # Тут указываем lang


def image_exists(image_field):
    if not image_field:
        return False
    image_path = os.path.join(settings.MEDIA_ROOT, image_field.name)
    return os.path.isfile(image_path)


def homepage(request, lang="uk"):

    sec_about_us = SectionAboutUs.objects.first()
    sec_events = SectionEvents.objects.first()

    sec_projects = SectionProjects.objects.first()
    sec_cta_first = CallToAction.objects.first()
    sec_cta_last = CallToAction.objects.last()

    events_objects = list(
        Events.objects.filter(show_in_main_page_carousel=True).order_by("order")
    )
    projects_objects = list(
        Projects.objects.filter(show_in_main_page_carousel=True).order_by("order")
    )

    carousel_objects = events_objects + projects_objects

    carousel_objects.sort(key=lambda x: x.order)

    context = {
        "events_objects": events_objects,
        "carousel_objects": carousel_objects,
        "sec_about_us": sec_about_us,
        "sec_events": sec_events,
        "sec_projects": sec_projects,
        "sec_cta_first": sec_cta_first,
        "sec_cta_last": sec_cta_last,
        "lang": lang,
    }

    return render(request, "homepage/homepage_index.html", context=context)
