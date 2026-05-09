"""Create a superuser from env if missing (for hosts without a shell, e.g. Render Free)."""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):
    help = (
        'If DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD are set, '
        'creates that superuser when it does not exist yet.'
    )

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '').strip() or f'{username}@localhost'

        if not username or not password:
            self.stdout.write(
                'Skipping: set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD to bootstrap admin.'
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists; left unchanged.'))
            return

        try:
            user = User(username=username, email=email, is_staff=True, is_superuser=True)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise CommandError(f'ensure_superuser failed: {e}') from e

        self.stdout.write(self.style.SUCCESS(f'Created superuser "{username}".'))
