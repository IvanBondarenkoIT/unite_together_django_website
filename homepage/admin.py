from django.contrib import admin
from .models import SectionAboutUs, SectionEvents, SectionProjects, CallToAction

admin.site.register(SectionAboutUs)
admin.site.register(SectionEvents)
admin.site.register(SectionProjects)
admin.site.register(CallToAction)
