from django.db import models

# Create your models here.
from django.db import models


class History(models.Model):
    title = models.CharField(max_length=255, default="History of Unite Together")
    content = models.TextField(default="")
    title_en = models.CharField(max_length=255, default="History of Unite Together")
    content_en = models.TextField(default="")
    image = models.ImageField(upload_to="img/partners", blank=True, null=True)

    def __str__(self):
        return self.title


class Mission(models.Model):
    title = models.CharField(max_length=255, default="Mission")
    content = models.TextField(default="")
    title_en = models.CharField(max_length=255, default="Mission")
    content_en = models.TextField(default="")

    def __str__(self):
        return self.title


class Vision(models.Model):
    title = models.CharField(max_length=255, default="Vision")
    content = models.TextField(default="")
    title_en = models.CharField(max_length=255, default="Vision")
    content_en = models.TextField(default="")

    def __str__(self):
        return self.title


class Value(models.Model):
    title = models.CharField(max_length=255, default="Values")
    content = models.TextField(default="")

    title_en = models.CharField(max_length=255, default="Values")
    content_en = models.TextField(default="")

    image = models.ImageField(upload_to="img/partners", blank=True, null=True)

    def __str__(self):
        return self.title


class Program(models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    support_partner = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    category_en = models.CharField(max_length=255, default="")
    title_en = models.CharField(max_length=255, default="")
    description_en = models.TextField(default="")
    support_partner_en = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    additional_info_en = models.TextField(blank=True, null=True, default="")

    beneficiaries_count = models.IntegerField(blank=True, null=True)
    funding_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    ordering_number = models.IntegerField(default=0)
    image = models.ImageField(upload_to="img/partners", blank=True, null=True)

    class Meta:
        ordering = [
            "ordering_number",
            "title",
        ]  # Default ordering by ordering_number, then title

    def __str__(self):
        return self.title


class DocumentCategory(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name


class Document(models.Model):
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)

    title_en = models.CharField(max_length=255, default="")
    subtitle_en = models.CharField(max_length=255, blank=True, null=True, default="")

    upload = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Partners(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    title_en = models.CharField(max_length=255, default="")
    description_en = models.TextField(blank=True, null=True, default="")

    image = models.ImageField(upload_to="img/partners", blank=True, null=True)
    url_link = models.URLField(blank=True, null=True)
    ordering_number = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Contacts(models.Model):
    # status
    status = models.BooleanField(default=True)
    # phone number
    phone_number = models.CharField(max_length=50)
    # email address
    email = models.EmailField()
    # address
    address = models.CharField(max_length=255)
    address_en = models.CharField(max_length=255, default="")
    # geolocation
    geolocation = models.CharField(max_length=255)
    # social media lincs
    instagram = models.URLField()
    facebook = models.URLField()
    telegram = models.URLField()

    def __str__(self):
        return self.email
