from django.db import migrations


FITMENTS = {
    "CV Joint": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Premium Cabin Air Filter": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "X-Trail", 2014, 2020),
    ],
    "High-Output Alternator 12V": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "AGM Car Battery 70Ah": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "CR-V", 2015, 2020),
        ("Nissan", "X-Trail", 2014, 2020),
    ],
    "Heavy-Duty Starter Motor": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Reinforced Serpentine Belt": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Silicone Radiator Hose": [
        ("Toyota", "RAV4", 2013, 2018),
        ("Honda", "CR-V", 2015, 2020),
        ("Nissan", "X-Trail", 2014, 2020),
    ],
    "Front Performance Shock Absorber": [
        ("Toyota", "RAV4", 2013, 2018),
        ("Honda", "CR-V", 2015, 2020),
        ("Nissan", "X-Trail", 2014, 2020),
    ],
    "Ceramic Front Brake Pad Set": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Synthetic Engine Oil Filter": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Civic", 2016, 2021),
    ],
    "High-Flow Engine Air Filter": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Brake Disc Rotor": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Toyota", "Camry", 2012, 2017),
    ],
    "Serpentine Belt Tensioner": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Clutch Master Cylinder": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Wheel Hub Assembly": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Toyota", "RAV4", 2013, 2018),
    ],
    "Outer Tie Rod End": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Suspension Control Arm": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Stabilizer Link Rod": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Honda", "CR-V", 2015, 2020),
    ],
    "Suspension Ball Joint": [
        ("Toyota", "RAV4", 2013, 2018),
        ("Honda", "CR-V", 2015, 2020),
        ("Nissan", "X-Trail", 2014, 2020),
    ],
    "Fuel Injector": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Civic", 2016, 2021),
    ],
    "Ignition Coil": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Radiator Fan Motor": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Thermostat Housing": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Civic", 2016, 2021),
    ],
    "AC Compressor": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Power Steering Pump": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Engine Mount": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
    "Engine Oil Pan": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Brake Caliper": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Toyota", "RAV4", 2013, 2018),
    ],
    "Timing Chain Kit": [
        ("Toyota", "Camry", 2012, 2017),
        ("Honda", "Accord", 2013, 2017),
        ("Nissan", "Altima", 2013, 2018),
    ],
    "Windshield Wiper Motor": [
        ("Toyota", "Corolla", 2014, 2019),
        ("Honda", "Civic", 2016, 2021),
        ("Nissan", "Sunny", 2014, 2019),
    ],
}


def seed_product_fitments(apps, schema_editor):
    Product = apps.get_model("myapp", "Product")
    ProductFitment = apps.get_model("myapp", "ProductFitment")

    for product_name, fitments in FITMENTS.items():
        product = Product.objects.filter(name=product_name).first()
        if not product:
            continue
        ProductFitment.objects.filter(product_id=product.id).delete()
        ProductFitment.objects.bulk_create(
            [
                ProductFitment(
                    product_id=product.id,
                    vehicle_make=make,
                    vehicle_model=model,
                    year_from=year_from,
                    year_to=year_to,
                )
                for make, model, year_from, year_to in fitments
            ]
        )
        make, model, year_from, _ = fitments[0]
        Product.objects.filter(id=product.id).update(
            vehicle=f"{make} {model}",
            vehicle_year=year_from,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0036_product_fitment"),
    ]

    operations = [
        migrations.RunPython(seed_product_fitments, migrations.RunPython.noop),
    ]
