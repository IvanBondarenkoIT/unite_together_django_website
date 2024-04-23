from django.db import models
from django.urls import reverse


# Create your models here.
class WebPage(models.Model):
    name = models.CharField(max_length=250)  # Events, Projects, AboutUs

    def __str__(self):
        return self.name


class ObjectsGroup(models.Model):  # Spotr, non-formal education, Events and master classes, Other
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    page = models.ForeignKey("WebPage", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.page}'

    def get_url(self):
        return reverse("events_by_group", args=[self.slug])



class WebContentObject(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='img/pages_content', blank=True)

    slug = models.SlugField(max_length=200, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey("ObjectsGroup", on_delete=models.CASCADE, blank=True, null=True)
    # web_page_owner = models.ForeignKey(WebPage, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.name} - {self.title}"



class WebContentSubordinateObject(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    text = models.TextField()
    image = models.ImageField(upload_to='img/pages_content_sub', blank=True)

    content_master_object = models.ForeignKey(WebContentObject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.title} - {self.text}"


class Events(WebContentObject):
    city = models.CharField(max_length=250, blank=True)
    start_age = models.IntegerField(blank=True, null=True)
    end_age = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self):
        return f"Event - {self.name}"

    def get_start_date_month(self):
        return self.start_date.strftime("%B")

    def get_url(self):
        return reverse("event_detail", args=[self.group.slug, self.slug])

    #
    # def get_date_year(self):


