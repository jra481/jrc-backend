from decimal import Decimal

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction

from myapp.models import (
    Brand,
    HeroBanner,
    HeroSideBanner,
    Product,
    ProductImage,
    ProductVariant,
    PromoBanner,
)


SPARE_PARTS = (
    {
        "name": "Front Brake Pad Set",
        "description": "Front disc brake pad set for routine brake service and dependable stopping performance.",
        "vehicle": "Toyota Corolla / Toyota Camry",
        "manufacturer": "Bosch",
        "price": "185.00",
        "stock": 24,
        "features": "Low-noise friction compound\nReliable braking performance\nFront axle replacement set",
    },
    {
        "name": "Engine Oil Filter",
        "description": "Spin-on engine oil filter for scheduled oil changes and everyday engine protection.",
        "vehicle": "Nissan Sunny / Nissan Altima",
        "manufacturer": "Mann-Filter",
        "price": "35.00",
        "stock": 60,
        "features": "Efficient oil filtration\nService-friendly fitment\nSuitable for routine maintenance",
    },
    {
        "name": "Engine Air Filter",
        "description": "Replacement engine air filter designed to maintain clean intake airflow during regular servicing.",
        "vehicle": "Honda Civic / Honda Accord",
        "manufacturer": "Denso",
        "price": "65.00",
        "stock": 45,
        "features": "Clean intake airflow\nDust and particle filtration\nDirect service replacement",
    },
    {
        "name": "Cabin Air Filter",
        "description": "Cabin air filter for cleaner passenger ventilation and climate-control maintenance.",
        "vehicle": "Toyota Corolla / Lexus ES",
        "manufacturer": "Mahle",
        "price": "55.00",
        "stock": 42,
        "features": "Cleaner cabin air\nHelps protect HVAC airflow\nEasy replacement fitment",
    },
    {
        "name": "Front Shock Absorber",
        "description": "Front suspension shock absorber for improved ride control and workshop replacement jobs.",
        "vehicle": "Nissan Patrol / Nissan X-Trail",
        "manufacturer": "KYB",
        "price": "420.00",
        "stock": 16,
        "features": "Front suspension fitment\nImproved ride control\nBuilt for daily road use",
    },
    {
        "name": "Serpentine Belt",
        "description": "Accessory drive belt for alternator, air-conditioning, and engine auxiliary systems.",
        "vehicle": "Toyota Camry / Toyota RAV4",
        "manufacturer": "Gates",
        "price": "95.00",
        "stock": 28,
        "features": "High-strength belt construction\nSupports auxiliary drive systems\nWorkshop replacement part",
    },
    {
        "name": "Car Battery 70Ah",
        "description": "Maintenance-free 12V battery for common passenger cars and light SUVs.",
        "vehicle": "12V passenger cars and SUVs",
        "manufacturer": "Varta",
        "price": "395.00",
        "stock": 12,
        "features": "70Ah capacity\nMaintenance-free design\nSuitable for everyday driving",
    },
    {
        "name": "Radiator Hose",
        "description": "High-temperature coolant hose for radiator and engine cooling-system service.",
        "vehicle": "Toyota Corolla / Toyota Yaris",
        "manufacturer": "Gates",
        "price": "80.00",
        "stock": 20,
        "features": "Heat-resistant rubber compound\nCooling-system replacement\nWorkshop-ready fitment",
    },
    {
        "name": "Alternator 12V",
        "description": "Replacement alternator for charging-system repairs and 12V electrical diagnostics.",
        "vehicle": "Nissan Patrol / Nissan Pathfinder",
        "manufacturer": "Valeo",
        "price": "780.00",
        "stock": 8,
        "features": "12V charging system\nStable electrical output\nReplacement unit for workshop repair",
    },
    {
        "name": "Starter Motor",
        "description": "Replacement starter motor for reliable engine cranking and petrol-engine workshop repairs.",
        "vehicle": "Ford Focus / Ford Escape",
        "manufacturer": "Denso",
        "price": "560.00",
        "stock": 9,
        "features": "Reliable engine cranking\n12V starter system\nWorkshop replacement component",
    },
)


class Command(BaseCommand):
    help = "Replace the current catalog and car-sale banner media with ten spare-part products."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Perform the catalog reset. Without this flag the command only previews the change.",
        )

    def handle(self, *args, **options):
        products = Product.objects.all()
        product_count = products.count()
        banner_count = (
            HeroBanner.objects.count()
            + HeroSideBanner.objects.count()
            + PromoBanner.objects.count()
        )
        self.stdout.write(
            f"Current catalog: {product_count} products, {banner_count} dynamic hero/promo banners."
        )
        self.stdout.write("New catalog: 10 active car spare-part products.")

        if not options["apply"]:
            self.stdout.write(self.style.WARNING("Preview only. Re-run with --apply to make the change."))
            return

        media_names = set(
            name
            for name in ProductImage.objects.values_list("image", flat=True)
            if name
        )
        media_names.update(
            name
            for name in products.values_list("promotional_banner_image", flat=True)
            if name
        )
        media_names.update(
            name
            for name in Brand.objects.values_list("logo", flat=True)
            if name
        )
        for model in (HeroBanner, HeroSideBanner, PromoBanner):
            media_names.update(
                name for name in model.objects.values_list("image", flat=True) if name
            )

        with transaction.atomic():
            # Product deletion cascades variants, images, related-product links,
            # and product views. There are no carts or orders in this local DB,
            # but their foreign keys remain protected by the model contract.
            Product.objects.all().delete()
            Brand.objects.all().delete()
            HeroBanner.objects.all().delete()
            HeroSideBanner.objects.all().delete()
            PromoBanner.objects.all().delete()

            brands = {}
            for item in SPARE_PARTS:
                manufacturer = item["manufacturer"]
                if manufacturer not in brands:
                    brands[manufacturer] = Brand.objects.create(
                        name=manufacturer,
                        is_active=True,
                    )

            for index, item in enumerate(SPARE_PARTS, start=1):
                product = Product.objects.create(
                    brand=brands[item["manufacturer"]],
                    vehicle=item["vehicle"],
                    manufacturer=item["manufacturer"],
                    name=item["name"],
                    description=item["description"],
                    key_features=item["features"],
                    shipping_fee=Decimal("0.00"),
                    estimated_delivery_time="2-5 working days",
                    seller_name="Jamal Rafeeq Auto Parts Trading LLC",
                    warranty_info="Supplier warranty; confirm fitment before installation.",
                    is_active=True,
                    related_product_mode=Product.RELATED_PRODUCT_MODE_NONE,
                )
                ProductVariant.objects.create(
                    product=product,
                    sku=f"JR-SP-{index:03d}",
                    price_type="single",
                    price=Decimal(item["price"]),
                    stock=item["stock"],
                )

        removed_files = 0
        for name in sorted(media_names):
            if default_storage.exists(name):
                default_storage.delete(name)
                removed_files += 1

        self.stdout.write(self.style.SUCCESS("Catalog reset complete."))
        self.stdout.write(f"Created {len(SPARE_PARTS)} spare-part products.")
        self.stdout.write(f"Removed {removed_files} old catalog/banner media files.")
