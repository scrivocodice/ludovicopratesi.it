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


PREVIEW_NAV_ITEMS = [
    {'href': '#hero', 'label': 'Home'},
    {'href': '#mostre', 'label': 'Mostre attive'},
    {'href': '#profilo', 'label': 'Profilo'},
    {'href': '#contatti', 'label': 'Contatti'},
]

PREVIEW_EXHIBITS = [
    {
        'modal_id': 'mostra-atlante',
        'category': 'Fotografia e installazione',
        'title': 'Atlante del Riflesso',
        'location': 'Palazzo Merulana, Roma',
        'period': '12 aprile - 30 giugno 2026',
        'summary': 'Un percorso immersivo tra archivi, luce e paesaggio urbano che mette in dialogo fotografia contemporanea e memoria dei luoghi.',
        'image': 'img/mostre/convento_3.jpeg',
        'details': [
            'Tre ambienti installativi con stampe di grande formato, proiezioni e materiali d’archivio.',
            'Programma pubblico con conversazioni, visite guidate e approfondimenti curatorali.',
            'Impianto visivo pensato per raccontare subito luogo, autori e periodo della mostra.',
        ],
    },
    {
        'modal_id': 'mostra-proiezioni',
        'category': 'Video e ricerca visiva',
        'title': 'Proiezioni d’Occidente',
        'location': 'Spazio Sala 1, Roma',
        'period': '5 maggio - 21 luglio 2026',
        'summary': 'Una selezione di opere video e immagini in movimento che indaga il rapporto tra identità visiva, architettura e costruzione del racconto.',
        'image': 'img/mostre/projection.jpg',
        'details': [
            'Allestimento modulare con pareti retroilluminate e schermi sospesi.',
            'Focus su pratiche interdisciplinari tra cinema sperimentale, fotografia e documentazione.',
            'La modale può ospitare testo curatoriale, orari, sede e una call to action futura.',
        ],
    },
    {
        'modal_id': 'mostra-paesaggi',
        'category': 'Percorso espositivo',
        'title': 'Paesaggi della Soglia',
        'location': 'Ex Convento, Napoli',
        'period': '18 settembre - 14 dicembre 2026',
        'summary': 'Una mostra costruita come attraversamento: immagini, testi e opere site-specific disegnano una soglia tra spazio intimo e visione pubblica.',
        'image': 'img/mostre/occidente.jpg',
        'details': [
            'Selezione di opere con taglio contemplativo e attenzione alla qualità fotografica.',
            'Scheda mostra sintetica in card, approfondimento completo nella modale Bootstrap.',
            'Impostazione adatta a trasformare il sito in una homepage unica con ancore interne.',
        ],
    },
]

PREVIEW_CONTACTS = {
    'email': 'info@ludovicopratesi.it',
    'address_lines': [
        'Studio curatoriale Ludovico Pratesi',
        'Via del Pellegrino 14',
        '00186 Roma',
    ],
}

PREVIEW_VARIANTS = {
    'one': {
        'page_title': 'Bozza 1 | Editoriale',
        'template_name': 'layout_previews/layout_preview_one.html',
        'current_preview': 'one',
        'draft_name': 'Bozza 1',
        'draft_style': 'Editoriale',
        'hero_image': 'img/mostre/convento.jpg',
        'hero_kicker': 'Single-page layout',
        'hero_title': 'Una home page elegante, lineare e focalizzata sui contenuti.',
        'hero_text': 'Navbar sempre visibile, fotografia a tutta larghezza e una gerarchia chiara per trasformare il sito in un racconto unico e continuo.',
        'hero_note': 'Questa direzione privilegia leggibilità, autorevolezza e un tono curatoriale sobrio.',
        'about_label': 'Impostazione',
        'about_title': 'Un ritmo editoriale che valorizza testi, immagini e approfondimenti.',
        'about_intro': 'La struttura è pensata per far convivere impatto visivo e chiarezza informativa. Le sezioni scorrono in modo naturale e ogni mostra ha una card ampia con modale dedicata.',
        'about_quote': 'La pagina funziona come un invito alla mostra: orienta, incuriosisce e poi approfondisce.',
        'about_points': [
            {
                'title': 'Hero fotografico',
                'text': 'La prima sezione usa una fotografia forte e un box testo sovrapposto per comunicare subito identità e posizionamento.',
            },
            {
                'title': 'Card ampie e ordinate',
                'text': 'Le mostre attive sono presentate in grandi blocchi orizzontali, con informazioni essenziali subito leggibili.',
            },
            {
                'title': 'Modali per i dettagli',
                'text': 'L’approfondimento si apre senza uscire dalla home, evitando ulteriori pagine pubbliche.',
            },
        ],
        'contacts_title': 'Contatti diretti',
        'contacts_intro': 'Nessun form in questa fase: la sezione finale mette in evidenza email e indirizzo, in continuità con il taglio essenziale della home.',
    },
    'two': {
        'page_title': 'Bozza 2 | Galleria',
        'template_name': 'layout_previews/layout_preview_two.html',
        'current_preview': 'two',
        'draft_name': 'Bozza 2',
        'draft_style': 'Galleria',
        'hero_image': 'img/mostre/convento_2.jpeg',
        'hero_kicker': 'Esperienza immersiva',
        'hero_title': 'Una homepage più scenografica, con forte impatto visivo.',
        'hero_text': 'Palette scura, contrasti netti e blocchi espositivi concepiti come locandine digitali che invitano al click e all’esplorazione.',
        'hero_note': 'Questa bozza lavora di atmosfera e rende la fotografia il motore principale della navigazione.',
        'about_label': 'Approccio',
        'about_title': 'Un taglio da galleria contemporanea con navigazione interna persistente.',
        'about_intro': 'Il layout usa fondi scuri, bordi luminosi e card ad alto contrasto. Il contenuto testuale è più selettivo, mentre il tono generale è più immersivo e istituzionale.',
        'about_quote': 'Qui il sito si comporta come una sala introduttiva: pochi elementi, grande presenza.',
        'about_points': [
            {
                'title': 'Navbar sempre in vista',
                'text': 'La barra resta fissa e leggera, con link di sezione sempre accessibili anche durante lo scroll.',
            },
            {
                'title': 'Mostre come poster',
                'text': 'Le card usano l’immagine come fondale e un pannello informativo sovrapposto con apertura modale.',
            },
            {
                'title': 'Testo più essenziale',
                'text': 'La parte centrale è costruita per raccontare visione e metodo con pochi elementi ma molta presenza tipografica.',
            },
        ],
        'contacts_title': 'Contatti e presenza',
        'contacts_intro': 'La chiusura del sito resta pulita e diretta, ma con un tono più istituzionale e una forte continuità cromatica con l’hero.',
    },
    'three': {
        'page_title': 'Bozza 3 | Atelier',
        'template_name': 'layout_previews/layout_preview_three.html',
        'current_preview': 'three',
        'draft_name': 'Bozza 3',
        'draft_style': 'Atelier',
        'hero_image': 'img/mostre/convento_3.jpeg',
        'hero_kicker': 'Tono caldo e materico',
        'hero_title': 'Una home page più umana e materica, con un carattere da studio.',
        'hero_text': 'Colori caldi, superfici morbide e un equilibrio tra racconto curatoriale, mostre attive e informazioni pratiche in una sola pagina.',
        'hero_note': 'Questa soluzione punta su prossimità, identità e riconoscibilità senza perdere chiarezza.',
        'about_label': 'Linguaggio',
        'about_title': 'Una direzione visiva più accogliente, pensata per costruire relazione.',
        'about_intro': 'La sezione testuale dopo le mostre è trattata come uno spazio editoriale più caldo. Blocchi, colori e spaziature suggeriscono un sito meno istituzionale e più personale.',
        'about_quote': 'La home diventa uno studio aperto: accoglie, orienta e invita ad approfondire.',
        'about_points': [
            {
                'title': 'Sezioni morbide',
                'text': 'Le superfici arrotondate e i fondi caldi danno al progetto un tono più intimo e contemporaneo.',
            },
            {
                'title': 'Card modulari',
                'text': 'Le mostre si leggono come blocchi autonomi ma coordinati, con molto spazio per un futuro storytelling editoriale.',
            },
            {
                'title': 'Contatti in evidenza',
                'text': 'La chiusura della pagina è semplice e molto chiara, pensata per agevolare il contatto immediato.',
            },
        ],
        'contacts_title': 'Studio e riferimenti',
        'contacts_intro': 'La sezione contatti usa un’impostazione essenziale, con dettagli pratici immediatamente leggibili e coerenti con il resto della pagina.',
    },
}


def _build_preview_context(variant_key):
    context = {
        'nav_items': PREVIEW_NAV_ITEMS,
        'exhibits': PREVIEW_EXHIBITS,
        'contacts': PREVIEW_CONTACTS,
    }
    context.update(PREVIEW_VARIANTS[variant_key])
    return context


def layout_preview_one(request):
    return render(
        request,
        PREVIEW_VARIANTS['one']['template_name'],
        _build_preview_context('one')
    )


def layout_preview_two(request):
    return render(
        request,
        PREVIEW_VARIANTS['two']['template_name'],
        _build_preview_context('two')
    )


def layout_preview_three(request):
    return render(
        request,
        PREVIEW_VARIANTS['three']['template_name'],
        _build_preview_context('three')
    )


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
