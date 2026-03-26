from datetime import date
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from easy_pdf.views import PDFTemplateView
from mail_templated import send_mail

from .forms import ContactForm
from .models import Contact, Exhibit, Resume, BoardItem


def homepage(request):
    curr_exhibits = Exhibit.objects.filter(
        begun_at__lte=date.today(),
        ended_at__gte=date.today()
    ).order_by('-ended_at')[:4]
    next_exhibits = Exhibit.objects.filter(
        begun_at__gt=date.today(),
    ).order_by('begun_at')[:4]
    boarditems = BoardItem.objects.all()
    return render(
        request,
        'homepage.html',
        {
            'curr_exhibits': curr_exhibits,
            'next_exhibits': next_exhibits,
            'boarditems': boarditems,
        }
    )


def exhibit_list(request):
    exhibits = Exhibit.objects.all().order_by('-ended_at')
    paginator = Paginator(exhibits, settings.ITEMS_PER_PAGE)
    page = request.GET.get('page')
    try:
        exhibit_list = paginator.page(page)
    except PageNotAnInteger:
        exhibit_list = paginator.page(1)
    except EmptyPage:
        exhibit_list = paginator.page(paginator.num_pages)
    return render(request,
        'exhibit_list.html',{'exhibit_list': exhibit_list}
    )

def exhibit_show(request, exhibit_slug):
    exhibit = get_object_or_404(Exhibit, slug=exhibit_slug)
    active_exhibits = Exhibit.objects.filter(
        begun_at__lte = date.today(), 
        ended_at__gte = date.today()
        ).order_by('-ended_at')
    past_exhibits = Exhibit.objects.filter( 
        ended_at__lt = date.today()
        ).order_by('-ended_at')
    return render(request, 'exhibit_show.html', {'exhibit':exhibit, 'active_exhibits': active_exhibits, 'past_exhibits': past_exhibits})

def resume(request):
    try:
        if hasattr(request, 'LANGUAGE_CODE'):
            resume = Resume.objects.get(lang=request.LANGUAGE_CODE)
        else:
            resume = Resume.objects.get(lang=settings.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        resume = None
    active_exhibits = Exhibit.objects.filter(
        begun_at__lte = date.today(), 
        ended_at__gte = date.today()
        ).order_by('-ended_at')
    return render(request, 'resume.html', {'resume': resume, 'active_exhibits': active_exhibits})

class ResumePdfView(PDFTemplateView):
    template_name = 'resume_pdf.html'

    def get_context_data(self, **kwargs):
        try:
            resume = Resume.objects.get(lang='it')
        except ObjectDoesNotExist as odne:
            resume = None
        return super(ResumePdfView, self).\
            get_context_data(resume=resume, encoding='utf-8', **kwargs)

class ResumeEnPdfView(PDFTemplateView):
    template_name = 'resume_pdf.html'

    def get_context_data(self, **kwargs):
        try:
            resume = Resume.objects.get(lang='en')
        except ObjectDoesNotExist as obne:
            resume = None
        return super(ResumeEnPdfView, self).\
            get_context_data(resume=resume, **kwargs)

def contacts(request):
    """
    manages contact form
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            contact = Contact()
            contact.subject = subject
            contact.message = message
            contact.sender_email = email
            contact.sender_name = name
            contact.save()

            from django.core.mail import BadHeaderError
            try:
                send_mail(
                    "email/thank_you_contact_to_owner.html",
                    {'contact': contact},
                    email,
                    [settings.EMAIL_CONTACT_ADDRESS]
                )
                template = "email/thank_you_contact_to_sender_%s.html" % \
                           request.LANGUAGE_CODE
                send_mail(template,
                    {'contact':contact},
                    settings.EMAIL_CONTACT_ADDRESS,
                    [email]
                )
                return HttpResponseRedirect(reverse('_thank_you_contact_us'))
            except BadHeaderError as bad_header:
                from django.contrib import messages
                messages.error(request, "Header non valido.")
    else:
        form = ContactForm()
    active_exhibits = Exhibit.objects.filter(
        begun_at__lte = date.today(),
        ended_at__gte = date.today()
        ).order_by('-ended_at')
    past_exhibits = Exhibit.objects.filter(
        ended_at__lt = date.today()
        ).order_by('-ended_at')
    return render(request, 'contacts.html',
        {
            'active_exhibits': active_exhibits,
            'past_exhibits': past_exhibits,
            'form': form,
        }
    )

def thank_you_contact_us(request):
    return render(request, 'contact_us_thank_you.html')
