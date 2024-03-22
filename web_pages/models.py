from django.db import models


# Create your models here.
class WebPage(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class WebContentObject(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='img/pages_content', blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    web_page_owner = models.ForeignKey(WebPage, on_delete=models.CASCADE, blank=True, null=True)

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





