from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


DEMO_VEHICLE_YEARS = {
    "Demo Car Sale 01 - City Compact Sedan": 2018,
    "Demo Car Sale 02 - Family SUV": 2019,
    "Demo Car Sale 03 - Executive Sedan": 2020,
    "Demo Car Sale 04 - Compact Crossover": 2021,
    "Demo Car Sale 05 - Electric Urban Hatchback": 2022,
    "Demo Car Sale 06 - Hybrid Family SUV": 2023,
    "Demo Car Sale 07 - Off-Road 4x4": 2020,
    "Demo Car Sale 08 - Performance Coupe": 2021,
    "Demo Car Sale 09 - Commercial Panel Van": 2019,
    "Demo Car Sale 10 - Seven Seat MPV": 2022,
    "Demo Car Sale 11 - Luxury Touring SUV": 2023,
    "Demo Car Sale 12 - Electric Delivery Van": 2024,
    "Demo Car Sale 13 - Pickup Utility Truck": 2018,
    "Demo Car Sale 14 - Compact City Hatchback": 2020,
    "Demo Car Sale 15 - Sport Touring Sedan": 2021,
    "Demo Vehicle 01 - Red City Sedan": 2024,
    "Demo Vehicle 02 - Black Family SUV": 2024,
    "Demo Vehicle 03 - Blue Sport Hatchback": 2024,
    "Demo Vehicle 04 - White Family Crossover": 2024,
}


def seed_demo_vehicle_years(apps, schema_editor):
    Product = apps.get_model("myapp", "Product")
    for name, year in DEMO_VEHICLE_YEARS.items():
        Product.objects.filter(name=name).update(vehicle_year=year)


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0034_seed_demo_brands"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="vehicle_year",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Vehicle model year, for example 2018.",
                null=True,
                validators=[MinValueValidator(1900), MaxValueValidator(2100)],
            ),
        ),
        migrations.RunPython(seed_demo_vehicle_years, migrations.RunPython.noop),
    ]
