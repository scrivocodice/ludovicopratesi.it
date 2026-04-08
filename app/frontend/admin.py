from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from .models import Exhibit, ExhibitImage


class ExhibitImageInline(admin.StackedInline):
    model = ExhibitImage
    extra = 1
    max_num = 3
    fields = ('image_thumb', 'is_thumbnail', 'filename')
    readonly_fields = ['image_thumb']


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '150'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 150})},
    }
    inlines = [ExhibitImageInline]
    list_display = ('title', 'authors', 'begun_at', 'ended_at')


@admin.register(ExhibitImage)
class ExhibitImageAdmin(admin.ModelAdmin):
    list_display = ('filename', 'item', 'is_thumbnail')
    list_select_related = ('item',)
