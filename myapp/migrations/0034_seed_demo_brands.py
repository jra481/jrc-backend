from django.db import migrations
from django.utils.text import slugify


DEMO_BRANDS = (
    "Toyota",
    "Nissan",
    "Honda",
    "BYD",
    "Ford",
    "Kia",
    "Lexus",
    "Maxus",
    "Isuzu",
    "Suzuki",
    "Mazda",
    "Bosch",
    "Mann-Filter",
    "Denso",
    "Mahle",
    "KYB",
    "Gates",
    "Varta",
    "Valeo",
    "SKF",
    "NGK",
    "Castrol",
    "Jamal Rafeeq Demo Motors",
)


def seed_demo_brands(apps, schema_editor):
    Brand = apps.get_model("myapp", "Brand")
    Product = apps.get_model("myapp", "Product")

    brands = {}
    for name in DEMO_BRANDS:
        brand, _ = Brand.objects.get_or_create(
            name=name,
            defaults={"slug": slugify(name), "is_active": True},
        )
        updates = []
        if not brand.slug:
            brand.slug = slugify(name)
            updates.append("slug")
        if not brand.is_active:
            brand.is_active = True
            updates.append("is_active")
        if updates:
            brand.save(update_fields=updates)
        brands[name] = brand

    # The demo catalogue already stores its supplier/manufacturer label on
    # each product. Use that value to populate the separate Brand relation so
    # the public Brand filter and the admin Brand field both have real data.
    for product in Product.objects.filter(
        name__startswith="Demo ",
        brand__isnull=True,
        manufacturer__in=DEMO_BRANDS,
    ):
        product.brand = brands[product.manufacturer]
        product.save(update_fields=["brand"])


def reverse_seed_demo_brands(apps, schema_editor):
    # Keep demo brands and assignments available for administrators to edit or
    # remove manually when reversing migrations.
    return None


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0033_seed_demo_vehicle_products"),
    ]

    operations = [
        migrations.RunPython(seed_demo_brands, reverse_seed_demo_brands),
    ]
