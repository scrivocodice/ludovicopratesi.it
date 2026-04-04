from django.conf import settings
from django.shortcuts import render
from django.utils.html import strip_tags

from .models import Exhibit


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
        'source_url': None,
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
        'source_url': None,
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
        'source_url': None,
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

HOME_PAGE = {
    'page_title': 'Ludovico Pratesi',
    'template_name': 'layout_previews/layout_preview_one.html',
    'hero_image': 'https://media.ludovicopratesi.it/thumbs/items/1b/f0/7a4deafc92387c03629cea08c419.jpg.637x388_q50_crop_smart_upscale.jpg',
    'hero_kicker': 'Curatore e critico d’arte',
    'hero_title': 'Mostre, profilo e contatti in una sola homepage.',
    'hero_text': 'Il sito raccoglie in una pagina unica il lavoro curatoriale, la traiettoria critica e una selezione delle mostre piu recenti, mantenendo una lettura chiara e diretta.',
    'hero_note': 'Le mostre restano al centro della navigazione, con profilo e riferimenti professionali integrati nello stesso racconto.',
    'about_label': 'Profilo',
    'about_title': 'Una pratica che tiene insieme curatela, critica e didattica.',
    'about_intro': 'Ludovico Pratesi e curatore e critico d’arte, docente allo IULM di Milano, direttore artistico di Spazio Taverna e voce storica del contemporaneo su La Repubblica.',
    'about_quote': 'Una ricerca curatoriale costruita tra mostre, istituzioni culturali, scrittura critica e formazione.',
    'about_points': [
        {
            'title': 'Spazio Taverna',
            'text': 'La direzione artistica di Spazio Taverna collega progetto curatoriale, committenze e attivazione dei luoghi.',
        },
        {
            'title': 'IULM Milano',
            'text': 'L’insegnamento di Didattica dell’arte rafforza la dimensione pubblica e formativa del lavoro.',
        },
        {
            'title': 'La Repubblica',
            'text': 'La scrittura critica accompagna l’attivita curatoriale e amplia il dialogo con il sistema dell’arte contemporanea.',
        },
    ],
    'contacts_title': 'Contatti diretti',
    'contacts_intro': 'Per richieste professionali e informazioni, i riferimenti restano accessibili in chiusura di pagina, senza percorsi separati.',
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
        .prefetch_related('images')
        .order_by('-ended_at', '-begun_at')
    )
    if exhibits:
        return [
            _serialize_exhibit_for_preview(exhibit, language_code)
            for exhibit in exhibits
        ]
    return PREVIEW_EXHIBITS


def _build_homepage_context(request):
    exhibit_items = _get_preview_exhibits(request)
    context = {
        'nav_items': PREVIEW_NAV_ITEMS,
        'exhibits': exhibit_items,
        'contacts': PREVIEW_CONTACTS,
        'initial_exhibits_count': INITIAL_EXHIBITS_COUNT,
        'has_more_exhibits': len(exhibit_items) > INITIAL_EXHIBITS_COUNT,
        'remaining_exhibits_count': max(len(exhibit_items) - INITIAL_EXHIBITS_COUNT, 0),
    }
    context.update(HOME_PAGE)
    return context


def homepage(request):
    return render(
        request,
        HOME_PAGE['template_name'],
        _build_homepage_context(request),
    )
