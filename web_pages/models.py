# import locale

from django.db import models
from django.urls import reverse


class BannerSettings(models.Model):
    about_us_banner_image = models.ImageField(upload_to="img/banners/")
    about_us_banner_mob_image = models.ImageField(upload_to="img/banners/")
    about_us_banner_title = models.CharField(max_length=255)
    about_us_banner_text = models.CharField(max_length=255)

    events_banner_image = models.ImageField(upload_to="img/banners/")
    events_banner_mob_image = models.ImageField(upload_to="img/banners/")
    events_banner_title = models.CharField(max_length=255)
    events_banner_text = models.CharField(max_length=255)

    projects_banner_image = models.ImageField(upload_to="img/banners/")
    projects_banner_mob_image = models.ImageField(upload_to="img/banners/")
    projects_banner_title = models.CharField(max_length=255)
    projects_banner_text = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Banner Settings"
        verbose_name_plural = "Banner Settings"

    def __str__(self):
        return f"{self.about_us_banner_title} {self.events_banner_title} {self.projects_banner_title}"


class City(models.Model):
    name = models.CharField(max_length=250)  # City name
    default_address = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


# Create your models here.
class WebPage(models.Model):
    name = models.CharField(max_length=250)  # Events, Projects, AboutUs

    def __str__(self):
        return self.name


class ObjectsGroup(
    models.Model
):  # Spotr, non-formal education, Events and master classes, Other
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    page = models.ForeignKey("WebPage", on_delete=models.CASCADE, blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name}"

    def get_url(self):
        return reverse(f"{self.page.name}_by_group", args=[self.slug])


class WebContentObject(models.Model):

    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="img/pages_content", blank=True, null=True)
    extra_details = models.TextField(blank=True, null=True)

    # Замените это поле
    selected_cities_list = models.ManyToManyField(
        City, blank=True, related_name="web_content_objects"
    )

    slug = models.SlugField(
        max_length=200, blank=True
    )  # slug  нужно сделать уникальным

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    show_in_main_page_carousel = models.BooleanField(default=False)

    group = models.ForeignKey(
        "ObjectsGroup", on_delete=models.CASCADE, blank=True, null=True
    )
    # web_page_owner = models.ForeignKey(WebPage, on_delete=models.CASCADE, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Events(WebContentObject):
    selected_city = models.ForeignKey(
        City, on_delete=models.CASCADE, blank=True, null=True
    )
    # city = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    start_age = models.IntegerField(blank=True, null=True)
    end_age = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    max_participants = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.name}"

    def get_start_date_year(self):
        if self.start_date:
            return self.start_date.strftime("%Y")
        else:
            return ""

    def get_start_date_month(self):
        if self.start_date:
            return self.start_date.strftime("%b")
        else:
            return ""

    def get_start_date_day(self):
        if self.start_date:
            return self.start_date.strftime("%d")
        else:
            return ""

    def get_url(self):
        return reverse("event_detail", args=[self.group.slug, self.slug])


class Projects(WebContentObject):
    selected_city = models.ForeignKey(
        City, on_delete=models.CASCADE, blank=True, null=True
    )
    # # city = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    start_age = models.IntegerField(blank=True, null=True)
    end_age = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    url_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Project - {self.name}"

    def get_start_date_year(self):
        if self.start_date:
            return self.start_date.strftime("%Y")
        else:
            return ""

    def get_start_date_month(self):
        if self.start_date:
            return self.start_date.strftime("%b")
        else:
            return ""

    def get_start_date_day(self):
        if self.start_date:
            return self.start_date.strftime("%d")
        else:
            return ""

    def get_end_date_year(self):
        return self.end_date.strftime("%Y")

    def get_end_date_month(self):
        # Устанавливаем украинскую локаль
        # locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
        return self.end_date.strftime("%b")

    def get_end_date_day(self):
        return self.end_date.strftime("%d")

    def get_url(self):
        return reverse("projects_detail", args=[self.group.slug, self.slug])


class ProjectGallery(models.Model):
    project = models.ForeignKey(Projects, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store/products/", max_length=255)

    def __str__(self):
        return self.project.name

    class Meta:
        verbose_name = "projectgallery"
        verbose_name_plural = "project gallerie"

    # class WebContentSubordinateObject(models.Model):
    #     name = models.CharField(max_length=250)
    #     title = models.CharField(max_length=250) #  must be max=27
    #     text = models.TextField()
    #     image = models.ImageField(upload_to='img/pages_content_sub', blank=True)
    #
    #     content_master_object = models.ForeignKey(WebContentObject, on_delete=models.CASCADE)
    #     is_active = models.BooleanField(default=True)
    #
    #     created_at = models.DateTimeField(auto_now_add=True)
    #
    #     def __str__(self):
    #         return f"{self.name} - {self.title} - {self.text}"
