from datetime import date
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.html import strip_tags
from easy_pdf.views import PDFTemplateView
from mail_templated import send_mail

from .forms import ContactForm
from .models import Contact, Exhibit, Resume, BoardItem


PREVIEW_NAV_ITEMS = [
    {'href': '#hero', 'label': 'Home'},
    {'href': '#mostre', 'label': 'Mostre'},
    {'href': '#profilo', 'label': 'Profilo'},
    {'href': '#contatti', 'label': 'Contatti'},
]

INITIAL_EXHIBITS_COUNT = 6

PREVIEW_EXHIBITS = [
    {
        'modal_id': 'mostra-antonio-marras',
        'category': 'Antonio Marras',
        'title': 'Vedere per Credere',
        'location': 'Forte Malatesta, Ascoli Piceno',
        'period': '8 marzo - 30 ottobre 2025',
        'summary': 'Un percorso immersivo tra celle, cortile e chiesa della Madonna del Lago rilegge il Forte Malatesta come una macchina del tempo fatta di ombre, memoria e trasformazione della materia.',
        'image_url': 'https://media.ludovicopratesi.it/thumbs/items/1b/f0/7a4deafc92387c03629cea08c419.jpg.637x388_q50_crop_smart_upscale.jpg',
        'source_url': 'https://ludovicopratesi.it/mostra/antonio-marras-vedere-credere',
        'details': [
            'La mostra intreccia la figura di Cecco d’Ascoli con la storia carceraria del Forte e con le sue presenze stratificate.',
            'Disegni, sculture, ceramiche e manufatti provenienti da Arquata costruiscono un allestimento di forte intensità narrativa.',
            'Il progetto, curato da Spazio Taverna, mette al centro stupore, meraviglia e riattivazione del genius loci.',
        ],
    },
    {
        'modal_id': 'mostra-marinella-senatore',
        'category': 'Marinella Senatore',
        'title': 'Murales',
        'location': 'Cantiere Metro C, Piazza Venezia, Roma',
        'period': '15 aprile - 31 agosto 2025',
        'summary': 'L’opera "Ci eleviamo sollevando gli altri" trasforma il cantiere di Piazza Venezia in una scena urbana dove infrastruttura, comunità e cultura diventano un unico racconto pubblico.',
        'image_url': 'https://media.ludovicopratesi.it/thumbs/items/44/fd/bee4e9bb396150df249e43490610.jpg.637x388_q50_crop_smart_upscale.jpg',
        'source_url': 'https://ludovicopratesi.it/mostra/marinella-senatore-murales',
        'details': [
            'La scheda del sito la presenta come la seconda opera del progetto Murales per la stazione di Piazza Venezia della Linea C.',
            'Il cantiere viene interpretato come palcoscenico teatrale e simbolo di una Roma che si rinnova attraverso collegamenti e relazioni.',
            'La mostra insiste sul valore culturale dello spazio pubblico e sul rapporto tra nuove infrastrutture e immaginario condiviso.',
        ],
    },
    {
        'modal_id': 'mostra-adigital-perspective',
        'category': 'Ginevra Petrozzi, Alessandro Giannì',
        'title': 'aDigital Perspective',
        'location': 'Istituto Italiano di Cultura, Belgrado',
        'period': '28 maggio - 20 agosto 2025',
        'summary': 'La terza tappa del progetto aDigital Perspective riunisce dieci artisti per esplorare il Tecnocene e le contraddizioni del digitale attraverso pratiche analogiche, ibride e installative.',
        'image_url': 'https://media.ludovicopratesi.it/thumbs/items/26/0e/91221e3ea719fb39acf245c30dce.jpg.637x388_q50_crop_smart_upscale.jpg',
        'source_url': 'https://ludovicopratesi.it/mostra/adigital-perspective',
        'details': [
            'La mostra coinvolge sei artisti italiani e quattro artisti dei Balcani in una piattaforma curatoriale itinerante.',
            'Pittura, installazione, fotografia e performance sono usate per affrontare il digitale senza facili ottimismi.',
            'Dal sito emerge anche la dimensione diplomatica del progetto, pensato per rafforzare i legami culturali tra Italia e Balcani.',
        ],
    },
]

PREVIEW_CONTACTS = {
    'email': 'lpratesi@futuronline.it',
    'address_lines': [
        'Via Principe Amedeo 126/b',
        '00185 Roma',
    ],
}

PREVIEW_VARIANTS = {
    'one': {
        'page_title': 'Bozza 1 | Editoriale',
        'template_name': 'layout_previews/layout_preview_one.html',
        'current_preview': 'one',
        'draft_name': 'Bozza 1',
        'draft_style': 'Editoriale',
        'hero_image': 'https://media.ludovicopratesi.it/thumbs/items/1b/f0/7a4deafc92387c03629cea08c419.jpg.637x388_q50_crop_smart_upscale.jpg',
        'hero_kicker': 'Curatore e critico d’arte',
        'hero_title': 'Una homepage unica che mette in fila mostre, profilo e contatti.',
        'hero_text': 'Dal Centro Arti Visive Pescheria di Pesaro a Spazio Taverna, il racconto del sito può concentrarsi in una sola pagina con una gerarchia chiara e un tono istituzionale.',
        'hero_note': 'Questa direzione mantiene un’impronta editoriale sobria e valorizza le mostre come cuore della navigazione.',
        'about_label': 'Profilo',
        'about_title': 'Una lettura ordinata dell’attività curatoriale e critica.',
        'about_intro': 'Il sito attuale presenta Ludovico Pratesi come curatore e critico d’arte, docente allo IULM di Milano, direttore artistico di Spazio Taverna e voce storica del contemporaneo su La Repubblica.',
        'about_quote': 'La singola home funziona bene quando il profilo professionale è forte e le mostre devono restare subito raggiungibili.',
        'about_points': [
            {
                'title': 'Spazio Taverna',
                'text': 'La direzione artistica di Spazio Taverna può stare al centro della presentazione, come chiave curatoriale che collega progetto, luoghi e committenze.',
            },
            {
                'title': 'IULM Milano',
                'text': 'Il ruolo di professore di Didattica dell’arte rafforza il profilo pubblico e aggiunge autorevolezza alla parte introduttiva della home.',
            },
            {
                'title': 'La Repubblica',
                'text': 'La dimensione critica e giornalistica può essere sintetizzata in poche righe, senza appesantire la navigazione con pagine separate.',
            },
        ],
        'contacts_title': 'Contatti diretti',
        'contacts_intro': 'La sezione finale riprende i contatti già presenti sul sito attuale e li mette in evidenza in modo più asciutto, senza form.',
    },
    'two': {
        'page_title': 'Bozza 2 | Galleria',
        'template_name': 'layout_previews/layout_preview_two.html',
        'current_preview': 'two',
        'draft_name': 'Bozza 2',
        'draft_style': 'Galleria',
        'hero_image': 'https://media.ludovicopratesi.it/thumbs/items/44/fd/bee4e9bb396150df249e43490610.jpg.637x388_q50_crop_smart_upscale.jpg',
        'hero_kicker': 'Mostre e progetti',
        'hero_title': 'Un taglio più scenografico, costruito attorno alle immagini delle mostre.',
        'hero_text': 'La navigazione resta in una sola pagina ma assume il ritmo di una galleria: grandi fondali, schede sintetiche e approfondimenti in modale per tenere il focus sugli eventi.',
        'hero_note': 'Questa bozza parte dall’archivio mostre del sito e lo traduce in una presenza più visiva e contemporanea.',
        'about_label': 'Percorso',
        'about_title': 'Un profilo curatoriale letto attraverso istituzioni, fondazioni e progetti.',
        'about_intro': 'Dalla direzione del Centro Arti Visive Pescheria di Pesaro alla Fondazione Guastalla e all’associazione Giovani Collezionisti, il sito attuale racconta un percorso lungo e articolato che qui viene reso più visivo.',
        'about_quote': 'Se il baricentro deve stare sulle mostre e sulla capacità di attivare luoghi, questo impianto è il più efficace.',
        'about_points': [
            {
                'title': 'Pescheria Pesaro',
                'text': 'Il lungo incarico di direzione artistica al Centro Arti Visive Pescheria può diventare uno dei cardini della sezione profilo.',
            },
            {
                'title': 'Fondazione Guastalla',
                'text': 'La dimensione della fondazione privata suggerisce un linguaggio più istituzionale, con attenzione a collezionismo e rete culturale.',
            },
            {
                'title': 'Giovani Collezionisti',
                'text': 'L’attività con l’associazione può trovare spazio in un blocco sintetico, utile a mostrare relazioni e progettualità più ampie.',
            },
        ],
        'contacts_title': 'Contatti e presenza',
        'contacts_intro': 'La chiusura resta asciutta ma più scenografica, con i riferimenti già pubblicati sul sito e un tono coerente con la sezione mostre.',
    },
    'three': {
        'page_title': 'Bozza 3 | Atelier',
        'template_name': 'layout_previews/layout_preview_three.html',
        'current_preview': 'three',
        'draft_name': 'Bozza 3',
        'draft_style': 'Atelier',
        'hero_image': 'https://media.ludovicopratesi.it/thumbs/items/26/0e/91221e3ea719fb39acf245c30dce.jpg.637x388_q50_crop_smart_upscale.jpg',
        'hero_kicker': 'Critica, didattica, curatela',
        'hero_title': 'Una direzione più personale, ma costruita su contenuti reali del sito.',
        'hero_text': 'La home accoglie biografia, mostre e contatti in un tono più caldo, senza perdere i riferimenti professionali che oggi definiscono il profilo di Ludovico Pratesi.',
        'hero_note': 'Qui il racconto è più vicino e narrativo, ma resta ancorato a incarichi, ruoli istituzionali e attività critica.',
        'about_label': 'Biografia',
        'about_title': 'Una narrazione più calda del percorso professionale.',
        'about_intro': 'Dalla Quadriennale di Roma ad AICA e AMACI, fino alla curatela scientifica di Palazzo Fabroni, questa bozza prova a rendere il profilo meno enciclopedico e più leggibile in una sola home.',
        'about_quote': 'Il sito può restare essenziale ma acquistare più carattere se la biografia viene trattata come un racconto, non come un elenco.',
        'about_points': [
            {
                'title': 'Quadriennale',
                'text': 'Il periodo come consigliere di amministrazione della Quadriennale d’Arte di Roma è uno snodo forte del percorso istituzionale.',
            },
            {
                'title': 'AICA e AMACI',
                'text': 'Le responsabilità associative raccontano un ruolo attivo dentro il sistema dell’arte contemporanea italiana.',
            },
            {
                'title': 'Palazzo Fabroni',
                'text': 'L’esperienza curatoriale a Pistoia aggiunge una dimensione museale che può essere sintetizzata senza appesantire la lettura.',
            },
        ],
        'contacts_title': 'Studio e riferimenti',
        'contacts_intro': 'I contatti vengono lasciati molto puliti, riprendendo email e indirizzo pubblicati sul sito ma inseriti in una chiusura più narrativa.',
    },
}

def _format_preview_date(value):
    if value is None:
        return ''
    return value.strftime('%d.%m.%Y')


def _get_preview_language(request):
    if hasattr(request, 'LANGUAGE_CODE'):
        return request.LANGUAGE_CODE
    return settings.LANGUAGE_CODE


def _get_exhibit_text(exhibit, language_code, excerpt=False):
    if language_code == 'en':
        text = exhibit.excerpt_en if excerpt else exhibit.description_en
        if text:
            return text
    return exhibit.excerpt_it if excerpt else exhibit.description_it


def _get_exhibit_image_url(exhibit):
    images = list(exhibit.images.all())
    if not images:
        return None
    image = None
    for exhibit_image in images:
        if exhibit_image.is_thumbnail:
            image = exhibit_image
            break
    if image is None:
        image = images[0]
    for alias in ('show', 'list', 'window'):
        try:
            return getattr(image.filename, alias).url
        except Exception:
            continue
    try:
        return image.filename.url
    except Exception:
        return None


def _serialize_exhibit_for_preview(exhibit, language_code):
    summary = _get_exhibit_text(exhibit, language_code, excerpt=True)
    if not summary:
        summary = strip_tags(_get_exhibit_text(exhibit, language_code) or '')[:240]
    authors = exhibit.get_authors() or 'Mostra'
    return {
        'modal_id': 'mostra-%s' % exhibit.slug,
        'category': authors,
        'title': exhibit.title,
        'location': exhibit.address,
        'period': '%s - %s' % (
            _format_preview_date(exhibit.begun_at),
            _format_preview_date(exhibit.ended_at),
        ),
        'summary': summary,
        'image_url': _get_exhibit_image_url(exhibit),
        'source_url': None,
        'description_html': _get_exhibit_text(exhibit, language_code) or '',
    }


def _get_preview_exhibits(request):
    language_code = _get_preview_language(request)
    exhibits = list(
        Exhibit.objects.all()
        .prefetch_related('authors', 'images')
        .order_by('-ended_at', '-begun_at')
    )
    if exhibits:
        return [
            _serialize_exhibit_for_preview(exhibit, language_code)
            for exhibit in exhibits
        ]
    return PREVIEW_EXHIBITS


def _build_preview_context(request, variant_key):
    exhibit_items = _get_preview_exhibits(request)
    context = {
        'nav_items': PREVIEW_NAV_ITEMS,
        'exhibits': exhibit_items,
        'contacts': PREVIEW_CONTACTS,
        'initial_exhibits_count': INITIAL_EXHIBITS_COUNT,
        'has_more_exhibits': len(exhibit_items) > INITIAL_EXHIBITS_COUNT,
        'remaining_exhibits_count': max(len(exhibit_items) - INITIAL_EXHIBITS_COUNT, 0),
    }
    context.update(PREVIEW_VARIANTS[variant_key])
    return context


def layout_preview_one(request):
    return render(
        request,
        PREVIEW_VARIANTS['one']['template_name'],
        _build_preview_context(request, 'one')
    )


def layout_preview_two(request):
    return render(
        request,
        PREVIEW_VARIANTS['two']['template_name'],
        _build_preview_context(request, 'two')
    )


def layout_preview_three(request):
    return render(
        request,
        PREVIEW_VARIANTS['three']['template_name'],
        _build_preview_context(request, 'three')
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
