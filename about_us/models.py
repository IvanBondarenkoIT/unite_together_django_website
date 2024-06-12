from django.db import models

# Create your models here.
from django.db import models


class History(models.Model):
    title = models.CharField(max_length=255, default="History of Unite Together")
    content = models.TextField()

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
