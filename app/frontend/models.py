# coding=utf-8
import hashlib
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField
from tinymce.models import HTMLField


class BoardItem(models.Model):
    message_it = models.TextField(blank=False, null=False)
    message_en = models.TextField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'board_item'
        verbose_name = 'Voce bacheca'
        verbose_name_plural = 'Voci bacheca'
        ordering = ['order', ]

    def __str__(self):
        return self.message_it


class Contact(models.Model):
    subject = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    sender_name = models.CharField(max_length=255, blank=False, null=False)
    sender_email = models.EmailField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'contact'


class Author(models.Model):
    first_name = models.CharField(
        _('first_name'),
        max_length=255,
        blank=True,
        null=True,
        help_text="Nome dell'artista. Massimo 255 caratteri")
    last_name = models.CharField(_('last_name'), max_length=255,
        help_text="Cognome dell'artista. Massimo 255 caratteri")

    def __str__(self):
        if self.first_name:
            return "%s %s" % (self.first_name.capitalize(), self.last_name.capitalize())
        else:
            return self.last_name.capitalize()

    class Meta:
        db_table = 'author'
        verbose_name = _('artist')
        verbose_name_plural = _('artists')

class Exhibit(models.Model):
    """
    Stores exhibits
    """
    title = models.CharField(_('title'),help_text='nome della mostra',\
        max_length=255)
    slug = models.SlugField(_('slug'),max_length=100,\
        help_text='nome della mostra sulla barra degli indirizzi(compilato automaticamente)',
        unique=True)

    excerpt_it = models.CharField(_('excerpt_it'),\
        help_text='breve descrizione della mostra',max_length=255,null=True,\
        blank=True, default="")
    description_it = HTMLField(_('description_it'),
        help_text='descrizione completa della mostra',)

    excerpt_en = models.CharField(_('excerpt_en'),
        help_text='breve descrizione della mostra(inglese)',\
        max_length=255, null=True, blank=True, default="")
    description_en = HTMLField(_('description_en'),
        help_text='descrizione completa della mostra(inglese)',)

    authors = models.ManyToManyField(Author,verbose_name=_("authors"),\
        help_text="autori della mostra",)
    address = models.CharField(_('address'),max_length=255,null=False,\
        blank=False,help_text="Indirizzo della mostra")
    begun_at = models.DateField(_('begun_at'),auto_now=False,blank=False,
        null=False,help_text="Data inizio mostra")
    ended_at = models.DateField(_('ended_at'),auto_now=False,blank=False,\
        null=False,help_text="Data fine mostra")

    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'exhibit'
        verbose_name = _('exhibit')
        verbose_name_plural = _('exhibits')

    def get_authors(self):
        """ concatenate exhibit authors divided by commas """
        res = None
        for author in self.authors.all():
            if res is None:
                res = "%s" % author
            else:
                res += ", %s" % author
        return res

    def get_thumbnail_image(self):
        """
        Returns first image with flag thumbnail set to True.
        First image otherwise
        """
        for image in self.images.all():
            if image.is_thumbnail:
                return image
        return self.images.all()[0]

def get_image_path(instance, filename):
    """Allows to save images on dynamic folders"""
    fileName, fileExtension = os.path.splitext(filename)
    fileExtension = fileExtension.lower()
    tohash = (instance.item.slug + fileName).encode('utf-8')
    md5_name = hashlib.md5(tohash).hexdigest() + fileExtension
    md5_path = os.path.join('items', md5_name[0:2], md5_name[2:4], md5_name[4:])
    md5_full_path = os.path.join(settings.MEDIA_ROOT, md5_path)
    if os.path.exists(md5_full_path):
        os.remove(md5_full_path)
    return md5_path

class ExhibitImage(models.Model):
    filename = ThumbnailerImageField(upload_to=get_image_path,
        verbose_name="Nome file",help_text="Inserire il file dell'immagine")
    item = models.ForeignKey(
        Exhibit, on_delete=models.CASCADE, related_name='images')
    is_thumbnail = models.BooleanField('immagine principale',default=False,\
        help_text="Se selezionata l'immagine sarà la principale della mostra")

    def __str__(self):
        return self.filename.name

    class Meta:
        db_table = 'exhibit_image'
        ordering = ['-is_thumbnail',]
        verbose_name = _('exhibit_image')
        verbose_name_plural = _('exhibit_images')

    def save(self):
        super(ExhibitImage, self).save()
        # compress image after uploading depending on image size
        if self.filename.size > 3072000:
            quality = int("20")
        else:
            quality = int("40")
        from PIL import Image as img
        name = str(self.filename.path)
        image_obj = img.open(name)
        image_obj.save(name, "JPEG", quality=quality, optimize=True)

    def image_thumb(self):
        """
        shows image thumbnails on django admin
        """
        if self.filename:
            return '<img src=%s%s width="100" height="100"/>' % (settings.MEDIA_URL, self.filename)
        else:
            return ''
    image_thumb.allow_tags = True
    image_thumb.short_description = "Anteprima immagine"

class Resume(models.Model):
    title = models.CharField(_("title"), help_text="Nome Cv", max_length=255)
    lang = models.CharField(_("language"), \
            help_text="Linguaggio utilizzato nel cv", max_length=2, \
            choices=settings.LANGUAGES)

    class Meta:
        db_table = 'resume'
        verbose_name = _('resume')
        verbose_name_plural = _('resumes')

    def __str__(self):
        return self.title


class ResumeSection(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        help_text="Selezionare il cv nel quale inserire la sezione",
        verbose_name=_("resume")
    )
    title = models.CharField(_("title"),
        help_text="Nome sezione", max_length=255, unique=True)
    description = HTMLField(_('description'),
        help_text='descrizione sezione',
        null=True, blank=True
    )
    position = models.PositiveIntegerField(_('position'),null=False, default=1,\
        help_text="Posizione della sezione all'interno del cv")

    class Meta:
        db_table = 'resume_section'
        verbose_name = _('resume_section')
        verbose_name_plural = _('resume_sections')
        unique_together = ('resume', 'title')
        ordering = ['position', 'title']

    def __str__(self):
        return self.title


class ResumeEvent(models.Model):
    section = models.ForeignKey(
        ResumeSection,
        on_delete=models.CASCADE,
        help_text="Selezionare la sezione nella quale inserire l'evento",
        verbose_name=_("resume_event")
    )
    begun_at = models.DateField(_('begun_at'),auto_now=False,blank=True,\
        null=True,help_text="Data iniziale dell'evento")
    ended_at = models.DateField(_('ended_at'),auto_now=False,blank=True,\
        null=True,help_text="Data finale dell'evento")
    title = models.CharField(_("title"),help_text="Nome evento",max_length=255)
    description = models.TextField(_('description'),\
        help_text='descrizione evento', blank=True, null=True)

    class Meta:
        db_table = 'resume_event'
        ordering = ['-begun_at', '-ended_at']
        verbose_name = _('resume_event')
        verbose_name_plural = _('resume_events')
        unique_together = ('section', 'title')

    def __str__(self):
        return self.title

    def get_date(self):
        if self.begun_at and self.ended_at:
            return "%s - %s" % (self.begun_at.strftime("%Y"), self.ended_at.strftime("%Y"))
        elif self.ended_at:
            return self.ended_at.strftime("%Y")
        elif self.begun_at:
            return self.begun_at.strftime("%Y")
        else:
            return None

    def resume(self):
        return self.section.resume

# generates thumbnails on item image saving
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)
