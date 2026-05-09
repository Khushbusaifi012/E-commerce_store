"""Create a superuser from env if missing (for hosts without a shell, e.g. Render Free)."""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()


class Command(BaseCommand):
    help = (
        'If DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD are set, '
        'creates that superuser when it does not exist yet. '
        'Set DJANGO_SUPERUSER_SYNC_PASSWORD=1 once to reset password / staff flags.'
    )

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '').strip() or f'{username}@localhost'
        sync_pw = os.getenv('DJANGO_SUPERUSER_SYNC_PASSWORD', '').lower() in (
            '1',
            'true',
            'yes',
        )

        if not username or not password:
            self.stdout.write(
                'Skipping: set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD to bootstrap admin.'
            )
            return

        existing = User.objects.filter(username=username).first()
        if existing:
            if sync_pw:
                try:
                    if email and existing.email != email:
                        existing.email = email
                    existing.is_staff = True
                    existing.is_superuser = True
                    existing.set_password(password)
                    existing.save()
                except Exception as e:
                    raise CommandError(f'ensure_superuser sync failed: {e}') from e
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated password and admin flags for "{username}". '
                        'Remove DJANGO_SUPERUSER_SYNC_PASSWORD from env after this deploy.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Superuser "{username}" already exists; left unchanged. '
                        'Set DJANGO_SUPERUSER_SYNC_PASSWORD=1 once if the password is wrong.'
                    )
                )
            return

        try:
            user = User(username=username, email=email, is_staff=True, is_superuser=True)
            user.set_password(password)
            user.save()
        except Exception as e:
            raise CommandError(f'ensure_superuser failed: {e}') from e

        self.stdout.write(self.style.SUCCESS(f'Created superuser "{username}".'))
