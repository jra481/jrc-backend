from pathlib import Path

from django.core.files import File
from django.db import migrations


DEMO_VEHICLES = (
    (
        "Demo Vehicle 01 - Red City Sedan",
        "Original-image demo vehicle listing for the Jamal Rafeeq automotive catalogue.",
        "New compact sedan demo vehicle",
        "Jamal Rafeeq Demo Motors",
        "Comfortable four-door sedan for city commuting and daily business use.",
        58000,
        2,
        "Demo Red",
        "#c62828",
        "DEMO-VEHICLE-01-RED",
        "demo-vehicle-red-sedan.png",
    ),
    (
        "Demo Vehicle 02 - Black Family SUV",
        "Original-image demo vehicle listing for the Jamal Rafeeq automotive catalogue.",
        "New family SUV demo vehicle",
        "Jamal Rafeeq Demo Motors",
        "Spacious five-door SUV demo with flexible passenger and cargo space.",
        96000,
        2,
        "Demo Black",
        "#171717",
        "DEMO-VEHICLE-02-BLACK",
        "demo-vehicle-black-suv.png",
    ),
    (
        "Demo Vehicle 03 - Blue Sport Hatchback",
        "Original-image demo vehicle listing for the Jamal Rafeeq automotive catalogue.",
        "New sporty hatchback demo vehicle",
        "Jamal Rafeeq Demo Motors",
        "Sporty five-door hatchback demo with an urban performance profile.",
        76000,
        3,
        "Demo Blue",
        "#1559d6",
        "DEMO-VEHICLE-03-BLUE",
        "demo-vehicle-blue-hatchback.png",
    ),
    (
        "Demo Vehicle 04 - White Family Crossover",
        "Original-image demo vehicle listing for the Jamal Rafeeq automotive catalogue.",
        "New family crossover demo vehicle",
        "Jamal Rafeeq Demo Motors",
        "Practical crossover demo with a raised driving position and family comfort.",
        88000,
        2,
        "Demo White",
        "#f5f5f5",
        "DEMO-VEHICLE-04-WHITE",
        "demo-vehicle-white-crossover.png",
    ),
)


def seed_demo_vehicle_products(apps, schema_editor):
    Product = apps.get_model("myapp", "Product")
    ProductVariant = apps.get_model("myapp", "ProductVariant")
    Color = apps.get_model("myapp", "Color")
    ProductImage = apps.get_model("myapp", "ProductImage")
    asset_root = Path(__file__).resolve().parents[1] / "seed_assets" / "demo_vehicles"

    for (
        name,
        description,
        vehicle,
        manufacturer,
        key_features,
        price,
        stock,
        color_name,
        color_code,
        sku,
        image_name,
    ) in DEMO_VEHICLES:
        product, _ = Product.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "vehicle": vehicle,
                "manufacturer": manufacturer,
                "key_features": key_features,
                "shipping_fee": 0,
                "estimated_delivery_time": "2-5 working days",
                "seller_name": "Jamal Rafeeq Demo Catalog",
                "warranty_info": "Demo listing - confirm warranty before sale.",
                "is_active": True,
            },
        )
        color, _ = Color.objects.get_or_create(name=color_name, defaults={"code": color_code})
        variant, _ = ProductVariant.objects.get_or_create(
            product=product,
            color=color,
            defaults={
                "sku": sku,
                "price_type": "single",
                "price": price,
                "stock": stock,
            },
        )
        if not ProductImage.objects.filter(variant=variant).exists():
            image_path = asset_root / image_name
            if not image_path.exists():
                raise FileNotFoundError(f"Missing demo vehicle asset: {image_path}")
            with image_path.open("rb") as image_file:
                ProductImage.objects.create(
                    variant=variant,
                    image=File(image_file, name=image_name),
                    is_primary=True,
                    position=0,
                )


def reverse_seed_demo_vehicle_products(apps, schema_editor):
    # Keep demo records and their generated images available for administrators
    # to edit or remove manually when reversing migrations.
    return None


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0032_seed_demo_automotive_products"),
    ]

    operations = [
        migrations.RunPython(
            seed_demo_vehicle_products,
            reverse_seed_demo_vehicle_products,
        ),
    ]
