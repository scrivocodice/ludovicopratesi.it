from html import unescape

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

PREVIEW_CONTACTS = {
    'email': 'ludovico@spaziotaverna.it',
    'address_lines': [
        'Viale Pola 6',
        '00198 Roma',
    ],
}

HOME_PAGE = {
    'page_title': 'Ludovico Pratesi',
    'template_name': 'layout_previews/layout_preview_one.html',
    'hero_image_static': 'img/hero2.webp',
    'hero_image': 'https://media.ludovicopratesi.it/thumbs/items/1b/f0/7a4deafc92387c03629cea08c419.jpg.637x388_q50_crop_smart_upscale.jpg',
    'hero_kicker': 'Ludovico Pratesi',
    'hero_title': 'Curatore e critico d’arte.',
    'hero_text': '',
    'hero_note': 'Fondatore e Direttore di Spazio Taverna.',
    'about_label': 'Profilo',
    'about_title': 'Una pratica che ha tenuto insieme curatela, critica e didattica.',
    'about_intro': 'Ludovico Pratesi è curatore e critico d’arte, direttore artistico di Spazio Taverna.',
    'about_quote': """
Nato nel 1961 a Roma, dove vive e lavora.

Nel 2020 ha fondato con Marco Bassan lo studio curatoriale Spazio Taverna.

Collabora con Artribune, ArtsLife, Arte Mondadori, Art Dossier e ArtNews.

Autore di saggi e pubblicazioni di arte contemporanea, tra cui monografie di Kounellis, Cattelan e Pistoletto.

È professore di Museologia del Contemporaneo all'Accademia di Belle Arti di Napoli.

Dal 2000 al 2017 è stato direttore artistico del Centro Arti Visive Pescheria di Pesaro.

Dal 1985 al 2025 ha collaborato a La Repubblica.
""".strip(),
    'about_feature_image_static': 'img/ritratto.webp',
    'about_feature_image': 'https://media.ludovicopratesi.it/thumbs/items/1b/f0/7a4deafc92387c03629cea08c419.jpg.637x388_q50_crop_smart_upscale.jpg',
    'about_feature_image_alt': 'Ludovico Pratesi in uno spazio espositivo di Spazio Taverna',
    'about_points': [
        {
            'title': 'Spazio Taverna',
            'text': 'La direzione artistica di Spazio Taverna collega progetto curatoriale, committenze e attivazione dei luoghi.',
        },
    ],
    'contacts_title': 'Contatti diretti',
    'contacts_intro': 'Per richieste professionali e informazioni, i riferimenti restano accessibili in chiusura di pagina, senza percorsi separati.',
}


def _format_preview_date(value):
    if value is None:
        return ''
    return value.strftime('%d.%m.%Y')


def _get_exhibit_text(exhibit, excerpt=False):
    return exhibit.excerpt if excerpt else exhibit.description


def _decode_html_entities(value):
    if not value:
        return ''
    return unescape(value).replace('\xa0', ' ')


def _normalize_plain_text(value):
    return ' '.join(_decode_html_entities(strip_tags(value or '')).split())


def _normalize_html_fragment(value):
    return _decode_html_entities(value)


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


def _serialize_exhibit_for_preview(exhibit):
    summary = _normalize_plain_text(_get_exhibit_text(exhibit, excerpt=True))
    if not summary:
        summary = _normalize_plain_text(_get_exhibit_text(exhibit))[:240]
    authors = _normalize_plain_text(exhibit.get_authors()) or 'Mostra'
    return {
        'modal_id': 'mostra-%s' % exhibit.slug,
        'category': authors,
        'title': _normalize_plain_text(exhibit.title),
        'location': _normalize_plain_text(exhibit.address),
        'period': '%s - %s' % (
            _format_preview_date(exhibit.begun_at),
            _format_preview_date(exhibit.ended_at),
        ),
        'summary': summary,
        'image_url': _get_exhibit_image_url(exhibit),
        'source_url': None,
        'description_html': _normalize_html_fragment(_get_exhibit_text(exhibit)),
    }


def _get_preview_exhibits():
    exhibits = list(
        Exhibit.objects.all()
        .prefetch_related('images')
    )
    return [
        _serialize_exhibit_for_preview(exhibit)
        for exhibit in exhibits
    ]


def _build_homepage_context(request):
    exhibit_items = _get_preview_exhibits()
    context = {
        'nav_items': PREVIEW_NAV_ITEMS,
        'exhibits': exhibit_items,
        'contacts': PREVIEW_CONTACTS,
        'google_analytics_measurement_id': getattr(settings, 'GOOGLE_ANALYTICS_MEASUREMENT_ID', ''),
        'static_version': getattr(settings, 'STATIC_VERSION', ''),
        'initial_exhibits_count': INITIAL_EXHIBITS_COUNT,
        'has_more_exhibits': len(exhibit_items) > INITIAL_EXHIBITS_COUNT,
        'remaining_exhibits_count': max(len(exhibit_items) - INITIAL_EXHIBITS_COUNT, 0),
    }
    context.update(HOME_PAGE)
    about_points = context.get('about_points') or []
    context['about_primary_point'] = about_points[0] if about_points else None
    return context


def homepage(request):
    return render(
        request,
        HOME_PAGE['template_name'],
        _build_homepage_context(request),
    )
