from django.contrib import admin
from .models import History, Mission, Vision, Value, Program, Partners
from .models import DocumentCategory, Document


admin.site.register(DocumentCategory)
admin.site.register(Document)

admin.site.register(Partners)

admin.site.register(History)
admin.site.register(Mission)
admin.site.register(Vision)
admin.site.register(Value)
admin.site.register(Program)
