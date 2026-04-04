# coding=utf-8
import hashlib
import os

from django.conf import settings
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField


class Exhibit(models.Model):
    """
    Stores exhibits.
    """

    title = models.CharField(
        _('title'),
        help_text='nome della mostra',
        max_length=255,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        help_text='nome della mostra sulla barra degli indirizzi(compilato automaticamente)',
        unique=True,
    )
    authors = models.TextField(
        _('authors'),
        help_text='autori della mostra',
        blank=True,
        default='',
    )
    excerpt_it = models.CharField(
        _('excerpt_it'),
        help_text='breve descrizione della mostra',
        max_length=255,
        null=True,
        blank=True,
        default='',
    )
    description_it = models.TextField(
        _('description_it'),
        help_text='descrizione completa della mostra',
    )
    excerpt_en = models.CharField(
        _('excerpt_en'),
        help_text='breve descrizione della mostra(inglese)',
        max_length=255,
        null=True,
        blank=True,
        default='',
    )
    description_en = models.TextField(
        _('description_en'),
        help_text='descrizione completa della mostra(inglese)',
    )
    address = models.CharField(
        _('address'),
        max_length=255,
        null=False,
        blank=False,
        help_text='Indirizzo della mostra',
    )
    begun_at = models.DateField(
        _('begun_at'),
        auto_now=False,
        blank=False,
        null=False,
        help_text='Data inizio mostra',
    )
    ended_at = models.DateField(
        _('ended_at'),
        auto_now=False,
        blank=False,
        null=False,
        help_text='Data fine mostra',
    )
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'exhibit'
        verbose_name = _('exhibit')
        verbose_name_plural = _('exhibits')

    def get_authors(self):
        return (self.authors or '').strip() or None

    def get_thumbnail_image(self):
        """
        Returns first image with flag thumbnail set to True.
        First image otherwise.
        """
        image = self.images.filter(is_thumbnail=True).first()
        if image is not None:
            return image
        return self.images.first()


def get_image_path(instance, filename):
    """Allows to save images on dynamic folders."""
    file_name, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()
    to_hash = (instance.item.slug + file_name).encode('utf-8')
    md5_name = hashlib.md5(to_hash).hexdigest() + file_extension
    md5_path = os.path.join('items', md5_name[0:2], md5_name[2:4], md5_name[4:])
    md5_full_path = os.path.join(settings.MEDIA_ROOT, md5_path)
    if os.path.exists(md5_full_path):
        os.remove(md5_full_path)
    return md5_path


class ExhibitImage(models.Model):
    filename = ThumbnailerImageField(
        upload_to=get_image_path,
        verbose_name='Nome file',
        help_text="Inserire il file dell'immagine",
    )
    item = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='images',
    )
    is_thumbnail = models.BooleanField(
        'immagine principale',
        default=False,
        help_text="Se selezionata l'immagine sarà la principale della mostra",
    )

    def __str__(self):
        return self.filename.name

    class Meta:
        db_table = 'exhibit_image'
        ordering = ['-is_thumbnail']
        verbose_name = _('exhibit_image')
        verbose_name_plural = _('exhibit_images')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.filename.size > 3072000:
            quality = 20
        else:
            quality = 40
        from PIL import Image as image_module

        name = str(self.filename.path)
        image_obj = image_module.open(name)
        image_obj.save(name, 'JPEG', quality=quality, optimize=True)

    def image_thumb(self):
        """
        Shows image thumbnails on django admin.
        """
        if not self.filename:
            return ''
        return format_html(
            '<img src="{}" width="100" height="100" />',
            self.filename.url,
        )

    image_thumb.short_description = 'Anteprima immagine'


from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.signals import saved_file

saved_file.connect(generate_aliases_global)
