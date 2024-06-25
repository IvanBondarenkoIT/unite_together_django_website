from django.db import models

from web_pages.models import WebContentObject


class Section(models.Model):
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='sections/', blank=True, null=True)
    # order = models.IntegerField(default=0, blank=True, null=True)
    link = models.URLField(blank=True, null=True)


#
class CallToAction(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)


class SectionAboutUs(Section):
    image = models.ImageField(upload_to='img/about_us', blank=True, null=True)

    def __str__(self):
        return self.title


class SectionEvents(Section):
    image = models.ImageField(upload_to='img/events', blank=True, null=True)

    def __str__(self):
        return self.title


class SectionProjects(Section):
    image = models.ImageField(upload_to='img/projects', blank=True, null=True)

    def __str__(self):
        return self.title

