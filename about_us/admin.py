from django.contrib import admin
from .models import History, Mission, Vision, Value, Program, Partners
from .models import DocumentCategory, Document, Contacts


class ContactsAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "status")
    list_filter = ("status",)
    search_fields = ("email", "phone_number", "address")
    fieldsets = (
        (
            "Contact Information",
            {"fields": ("status", "email", "phone_number", "address", "address_en")},
        ),
        (
            "Social Media",
            {"fields": ("instagram", "facebook", "telegram"), "classes": ("collapse",)},
        ),
        ("Location", {"fields": ("geolocation",)}),
    )


admin.site.register(DocumentCategory)
admin.site.register(Document)

admin.site.register(Partners)

admin.site.register(History)
admin.site.register(Mission)
admin.site.register(Vision)
admin.site.register(Value)
admin.site.register(Program)
admin.site.register(Contacts, ContactsAdmin)
