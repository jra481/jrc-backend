from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from myapp.models import Product, ProductImage


IMAGE_SETS = {
    "Front Brake Pad Set": (
        "front-brake-pad-set-01.png",
        "front-brake-pad-set-02.png",
        "front-brake-pad-set-03.png",
    ),
    "Engine Oil Filter": (
        "engine-oil-filter-01.png",
        "engine-oil-filter-02.png",
        "engine-oil-filter-03.png",
    ),
    "Engine Air Filter": (
        "engine-air-filter-01.png",
        "engine-air-filter-02.png",
        "engine-air-filter-03.png",
    ),
    "Cabin Air Filter": (
        "cabin-air-filter-01.png",
        "cabin-air-filter-02.png",
        "cabin-air-filter-03.png",
    ),
    "Front Shock Absorber": (
        "front-shock-absorber-01.png",
        "front-shock-absorber-02.png",
        "front-shock-absorber-03.png",
    ),
    "Serpentine Belt": (
        "serpentine-belt-01.png",
        "serpentine-belt-02.png",
        "serpentine-belt-03.png",
    ),
    "Car Battery 70Ah": (
        "car-battery-70ah-01.png",
        "car-battery-70ah-02.png",
        "car-battery-70ah-03.png",
    ),
    "Radiator Hose": (
        "radiator-hose-01.png",
        "radiator-hose-02.png",
        "radiator-hose-03.png",
    ),
    "Alternator 12V": (
        "alternator-12v-01.png",
        "alternator-12v-02.png",
        "alternator-12v-03.png",
    ),
    "Starter Motor": (
        "starter-motor-01.png",
        "starter-motor-02.png",
        "starter-motor-03.png",
    ),
}


class Command(BaseCommand):
    help = "Attach the three generated catalog images to each spare-part product."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Create the product-image records. Without this flag the command only previews the change.",
        )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT) / "products" / "spare-parts"
        missing = [
            str(media_root / filename)
            for filenames in IMAGE_SETS.values()
            for filename in filenames
            if not (media_root / filename).exists()
        ]
        if missing:
            raise CommandError(f"Missing spare-part media files: {', '.join(missing)}")

        products = {product.name: product for product in Product.objects.filter(name__in=IMAGE_SETS)}
        missing_products = sorted(set(IMAGE_SETS) - set(products))
        if missing_products:
            raise CommandError(f"Missing spare-part products: {', '.join(missing_products)}")

        existing_count = ProductImage.objects.filter(variant__product__name__in=IMAGE_SETS).count()
        self.stdout.write(
            f"Ready to attach {sum(len(files) for files in IMAGE_SETS.values())} images to {len(IMAGE_SETS)} products."
        )
        if existing_count:
            raise CommandError(
                f"Found {existing_count} existing product-image records. Refusing to duplicate or replace them."
            )
        if not options["apply"]:
            self.stdout.write(self.style.WARNING("Preview only. Re-run with --apply to make the change."))
            return

        with transaction.atomic():
            for product_name, filenames in IMAGE_SETS.items():
                product_variants = list(products[product_name].variants.order_by("id")[:1])
                if not product_variants:
                    raise CommandError(f"Product has no variant: {product_name}")
                variant = product_variants[0]
                for position, filename in enumerate(filenames):
                    ProductImage.objects.create(
                        variant=variant,
                        image=f"products/spare-parts/{filename}",
                        is_primary=position == 0,
                        position=position,
                    )

        self.stdout.write(self.style.SUCCESS("Attached three images to every spare-part product."))
