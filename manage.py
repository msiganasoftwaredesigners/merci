#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    environment = os.environ.get('ENVIRONMENT', 'development')
    settings_module = 'msigana_ecommerce.settings.dev' if environment == 'development' else 'msigana_ecommerce.settings.production'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
