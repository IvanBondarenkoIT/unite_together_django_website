from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from web_pages.forms import ProjectsForm, EventsForm
from web_pages.models import WebPage, WebContentObject, WebContentSubordinateObject, Events, ObjectsGroup, City, \
    Projects


# Register your models here.

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_address')


class WebPageAdmin(admin.ModelAdmin):
    list_display = ('name',)


class WebContentObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active', )
    prepopulated_fields = {'slug': ('name',)}


class WebContentSubordinateObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'text',)


# +
class PageTypeListFilter(admin.SimpleListFilter):
    title = _('Page Type')
    parameter_name = 'page_type'

    def lookups(self, request, model_admin):
        return (
            ('projects', _('Projects')),
            ('events', _('Events')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'projects':
            return queryset.filter(page__name__iexact='projects')
        if self.value() == 'events':
            return queryset.filter(page__name__iexact='events')
        return queryset


class ObjectsGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (PageTypeListFilter,)


class ProjectsAdmin(admin.ModelAdmin):
    form = ProjectsForm
    list_display = ('name', 'title', 'text', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name', 'group')}


class EventsAdmin(admin.ModelAdmin):
    form = EventsForm
    list_display = ('name', 'title', 'text', 'is_active', 'created_at', 'updated_at',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name', 'group')}


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Events, EventsAdmin)


# -

admin.site.register(City, CityAdmin)
admin.site.register(WebPage, WebPageAdmin)
admin.site.register(WebContentObject, WebContentObjectAdmin)
admin.site.register(WebContentSubordinateObject, WebContentSubordinateObjectAdmin)
admin.site.register(ObjectsGroup, ObjectsGroupAdmin)

