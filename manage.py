#!/usr/bin/env python
import os
import sys


def normalize_legacy_django_argv(argv):
    if len(argv) < 3 or not argv[1].startswith("-"):
        return argv

    command_index = None
    for index, value in enumerate(argv[1:], start=1):
        if not value.startswith("-"):
            command_index = index
            break

    if command_index is None or command_index == 1:
        return argv

    return [
        argv[0],
        argv[command_index],
        *argv[1:command_index],
        *argv[command_index + 1:],
    ]


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings.loc")

    from django.core.management import execute_from_command_line

    execute_from_command_line(normalize_legacy_django_argv(sys.argv))
