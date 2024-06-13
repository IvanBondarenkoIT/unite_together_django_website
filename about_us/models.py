from django.db import models

# Create your models here.
from django.db import models


class History(models.Model):
    title = models.CharField(max_length=255, default="History of Unite Together")
    content = models.TextField()
    image = models.ImageField(upload_to='img/partners', blank=True, null=True)

    def __str__(self):
        return self.title


class Mission(models.Model):
    title = models.CharField(max_length=255, default="Mission")
    content = models.TextField()

    def __str__(self):
        return self.title


class Vision(models.Model):
    title = models.CharField(max_length=255, default="Vision")
    content = models.TextField()

    def __str__(self):
        return self.title


class Value(models.Model):
    title = models.CharField(max_length=255, default="Values")
    content = models.TextField()
    image = models.ImageField(upload_to='img/partners', blank=True, null=True)

    def __str__(self):
        return self.title


class Program(models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    support_partner = models.CharField(max_length=255, blank=True, null=True)
    beneficiaries_count = models.IntegerField(blank=True, null=True)
    funding_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class DocumentCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Document(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    upload = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Partners(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='img/partners', blank=True, null=True)
    url_link = models.URLField(blank=True, null=True)