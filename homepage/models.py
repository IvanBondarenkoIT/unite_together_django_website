from django.db import models


class Section(models.Model):
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


#
class CallToAction(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='img/homepage', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class SectionAboutUs(Section):
    image = models.ImageField(upload_to='img/about_us', blank=True, null=True)


class SectionEvents(Section):
    image = models.ImageField(upload_to='img/events', blank=True, null=True)


class SectionProjects(Section):
    image = models.ImageField(upload_to='img/projects', blank=True, null=True)



