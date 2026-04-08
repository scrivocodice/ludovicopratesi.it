#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


LEGACY_MODELS_TO_DROP = {
    'frontend.author',
    'frontend.boarditem',
    'frontend.contact',
    'frontend.resume',
    'frontend.resumeevent',
    'frontend.resumesection',
}


def normalize_model_name(value):
    return value.lower()


def build_author_map(objects):
    author_map = {}

    for obj in objects:
        if normalize_model_name(obj.get('model', '')) != 'frontend.author':
            continue

        fields = obj.get('fields', {})
        first_name = (fields.get('first_name') or '').strip()
        last_name = (fields.get('last_name') or '').strip()

        if first_name and last_name:
            full_name = '%s %s' % (first_name.capitalize(), last_name.capitalize())
        elif last_name:
            full_name = last_name.capitalize()
        else:
            full_name = first_name.capitalize()

        author_map[obj.get('pk')] = full_name

    return author_map


def normalize_exhibit_fields(fields, author_map, blank_missing_authors=False):
    if 'excerpt' not in fields and 'excerpt_it' in fields:
        fields['excerpt'] = fields['excerpt_it']
    fields.pop('excerpt_it', None)

    if 'description' not in fields and 'description_it' in fields:
        fields['description'] = fields['description_it']
    fields.pop('description_it', None)

    fields.pop('excerpt_en', None)
    fields.pop('description_en', None)

    authors = fields.get('authors')
    if isinstance(authors, list):
        if authors and not author_map:
            if blank_missing_authors:
                fields['authors'] = ''
                return fields
            raise ValueError(
                'Il fixture contiene authors come lista di PK, ma non contiene i record '
                'frontend.Author necessari per convertirli. '
                'Rigenera il dump includendo frontend.Author oppure usa '
                '--blank-missing-authors per importare comunque svuotando authors.'
            )

        names = []
        missing = []
        for author_pk in authors:
            name = author_map.get(author_pk)
            if name:
                names.append(name)
            else:
                missing.append(author_pk)

        if missing:
            raise ValueError(
                'Impossibile convertire gli autori con PK %s: mancano dal fixture.'
                % ', '.join(str(value) for value in missing)
            )

        fields['authors'] = ', '.join(names)

    return fields


def normalize_fixture(objects, blank_missing_authors=False):
    author_map = build_author_map(objects)
    normalized = []

    for obj in objects:
        model_name = normalize_model_name(obj.get('model', ''))

        if model_name in LEGACY_MODELS_TO_DROP:
            continue

        new_obj = {
            'model': obj.get('model'),
            'pk': obj.get('pk'),
            'fields': dict(obj.get('fields', {})),
        }

        if model_name == 'frontend.exhibit':
            new_obj['fields'] = normalize_exhibit_fields(
                new_obj['fields'],
                author_map,
                blank_missing_authors=blank_missing_authors,
            )

        normalized.append(new_obj)

    return normalized


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            'Normalizza un dumpdata vecchio per il nuovo schema delle mostre: '
            'rinomina excerpt_it/description_it, elimina i campi inglesi e '
            'rimuove i modelli legacy.'
        )
    )
    parser.add_argument('input', help='Fixture JSON sorgente')
    parser.add_argument(
        'output',
        nargs='?',
        help='Fixture JSON normalizzato. Se omesso usa <input>.normalized.json',
    )
    parser.add_argument(
        '--blank-missing-authors',
        action='store_true',
        help=(
            'Se authors e una lista di PK ma nel dump mancano i record frontend.Author, '
            'svuota il campo authors invece di fallire.'
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix('.normalized.json')

    with input_path.open('r', encoding='utf-8') as handle:
        objects = json.load(handle)

    normalized = normalize_fixture(
        objects,
        blank_missing_authors=args.blank_missing_authors,
    )

    with output_path.open('w', encoding='utf-8') as handle:
        json.dump(normalized, handle, indent=2, ensure_ascii=False)
        handle.write('\n')

    print(output_path)


if __name__ == '__main__':
    main()
