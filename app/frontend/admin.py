from django.db import models
from django.contrib import admin
from django.forms import TextInput
from tinymce.widgets import TinyMCE
from .models import Author, Exhibit, ExhibitImage, Resume, ResumeEvent, ResumeSection
from .models import BoardItem


class BoardItemAdmin(admin.ModelAdmin):
    list_display = ('message_it', 'message_en', 'order')

class AuthorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "150"})}
    }
    list_display = ('last_name', 'first_name',)


class ExhibitImageAdmin(admin.StackedInline):
    model = ExhibitImage
    extra = 1
    max_num = 3
    fields = ('image_thumb', 'is_thumbnail', 'filename',),
    readonly_fields = ['image_thumb']


class ExhibitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('authors',)
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "150"})},
    }
    inlines = [ExhibitImageAdmin, ]
    list_display = ('title', 'begun_at', 'ended_at',)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang',)


class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'resume', 'position')


class ResumeEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'resume')

admin.site.register(Exhibit, ExhibitAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(ResumeSection, ResumeSectionAdmin)
admin.site.register(ResumeEvent, ResumeEventAdmin)
admin.site.register(BoardItem, BoardItemAdmin)
