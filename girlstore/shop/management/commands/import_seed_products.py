"""Load products + images from fixtures when the DB has no products yet (e.g. first deploy)."""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from shop.models import Product

FIXTURE_PATH = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'products.json'
SEED_IMAGES_DIR = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'product_images'


class Command(BaseCommand):
    help = (
        'If there are no products yet and shop/fixtures/products.json exists, '
        'run loaddata and copy shop/fixtures/product_images/* into MEDIA_ROOT.'
    )

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write('Products already exist; skipping import_seed_products.')
            return

        if not FIXTURE_PATH.is_file():
            self.stdout.write(
                f'No fixture at {FIXTURE_PATH}; skipping. '
                '(Generate with: python manage.py dumpdata shop.Product --indent 2 -o shop/fixtures/products.json)'
            )
            return

        call_command('loaddata', 'products', verbosity=1)

        dest = Path(settings.MEDIA_ROOT) / 'product_images'
        dest.mkdir(parents=True, exist_ok=True)

        if SEED_IMAGES_DIR.is_dir():
            for f in SEED_IMAGES_DIR.iterdir():
                if f.is_file():
                    shutil.copy2(f, dest / f.name)
            self.stdout.write(self.style.SUCCESS(f'Copied images into {dest}'))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'No {SEED_IMAGES_DIR}; product rows loaded but images may 404 until you upload in admin.'
                )
            )
