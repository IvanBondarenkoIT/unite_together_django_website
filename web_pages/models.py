from django.db import models


# Create your models here.


class WebContentObject(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='img/pages_content', blank=True)
        
    subordinate_objects = models.ManyToManyField('self', symmetrical=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.title} - {self.text}"


class WebContentSubordinateObject(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    text = models.TextField()
    image = models.ImageField(upload_to='img/pages_content_sub', blank=True)

    content_master_object = models.ForeignKey(WebContentObject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.title} - {self.text}"


class WebPage(models.Model):
    name = models.CharField(max_length=250)

    # friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self):
        return self.name


class WebPageSection(models.Model):
    name = models.CharField(max_length=250)
    page = models.ForeignKey(WebPage, on_delete=models.CASCADE)
    content = models.ForeignKey(WebContentObject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.page} - {self.content}"
