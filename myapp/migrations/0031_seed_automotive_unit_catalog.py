from django.db import migrations


AUTOMOTIVE_UNIT_TYPES = (
    (
        "Quantity",
        "Counts for vehicles, spare parts, kits, sets, and packaged items.",
        (
            ("Piece", "pcs", "One individual vehicle or spare part."),
            ("Set", "set", "A matching set of parts sold together."),
            ("Pair", "pair", "Two matching parts sold together."),
            ("Kit", "kit", "A service or repair kit."),
            ("Pack", "pack", "A packaged quantity of parts or consumables."),
        ),
    ),
    (
        "Mileage",
        "Distance readings used for vehicle listings, service intervals, and warranties.",
        (
            ("Kilometre", "km", "Metric vehicle distance."),
            ("Mile", "mi", "Imperial vehicle distance."),
        ),
    ),
    (
        "Engine Capacity",
        "Engine displacement values used in vehicle sales and fitment information.",
        (
            ("Cubic centimetre", "cc", "Engine displacement in cubic centimetres."),
            ("Litre", "L", "Engine displacement in litres."),
        ),
    ),
    (
        "Volume",
        "Fluid quantities for engine oil, coolant, brake fluid, fuel, and workshop supplies.",
        (
            ("Litre", "L", "Workshop and vehicle fluid volume."),
            ("Millilitre", "ml", "Small fluid volume."),
        ),
    ),
    (
        "Weight",
        "Weights for parts, batteries, tyres, freight, and workshop materials.",
        (
            ("Kilogram", "kg", "Automotive and shipping weight."),
            ("Gram", "g", "Small part or material weight."),
        ),
    ),
    (
        "Length",
        "Dimensions for belts, hoses, cables, fasteners, and other spare parts.",
        (
            ("Millimetre", "mm", "Small automotive dimension."),
            ("Centimetre", "cm", "Automotive dimension."),
            ("Metre", "m", "Long cable, hose, or material length."),
        ),
    ),
    (
        "Pressure",
        "Tyre, hydraulic, air-conditioning, and workshop pressure measurements.",
        (
            ("Bar", "bar", "Common workshop pressure unit."),
            ("PSI Pressure", "psi", "Pressure used for tyres and service equipment."),
        ),
    ),
    (
        "Voltage",
        "Electrical voltage values for batteries, chargers, sensors, and vehicle systems.",
        (
            ("Volt", "V", "Automotive electrical voltage."),
        ),
    ),
    (
        "Current",
        "Electrical current values for batteries, chargers, fuses, and vehicle systems.",
        (
            ("Ampere", "A", "Automotive electrical current."),
        ),
    ),
    (
        "Battery Capacity",
        "Battery capacity values for vehicle batteries and electrical accessories.",
        (
            ("Ampere hour", "Ah", "Battery charge capacity."),
        ),
    ),
    (
        "Power",
        "Vehicle and component power ratings used in sales and technical specifications.",
        (
            ("Kilowatt", "kW", "Metric engine or motor power."),
            ("Horsepower", "hp", "Vehicle power rating."),
        ),
    ),
    (
        "Torque",
        "Torque values used for vehicle specifications and workshop tightening settings.",
        (
            ("Newton metre", "Nm", "Vehicle and fastener torque."),
        ),
    ),
    (
        "Temperature",
        "Temperature values used for cooling systems, engines, tyres, and workshop checks.",
        (
            ("Degree Celsius", "°C", "Metric automotive temperature."),
        ),
    ),
    (
        "Time",
        "Time units used for labour, service duration, warranty periods, and delivery estimates.",
        (
            ("Minute", "min", "Short workshop or service duration."),
            ("Hour", "hr", "Labour or service duration."),
            ("Day", "day", "Delivery, warranty, or service period."),
        ),
    ),
)


def seed_automotive_unit_catalog(apps, schema_editor):
    UnitType = apps.get_model("myapp", "UnitType")
    Unit = apps.get_model("myapp", "Unit")

    for type_name, type_description, units in AUTOMOTIVE_UNIT_TYPES:
        unit_type, _ = UnitType.objects.get_or_create(name=type_name)
        if not unit_type.description:
            unit_type.description = type_description
            unit_type.save(update_fields=["description"])

        for unit_name, symbol, description in units:
            unit, created = Unit.objects.get_or_create(
                unit_type=unit_type,
                name=unit_name,
                defaults={"symbol": symbol, "description": description},
            )
            if not created:
                updates = []
                if not unit.symbol:
                    unit.symbol = symbol
                    updates.append("symbol")
                if not unit.description:
                    unit.description = description
                    updates.append("description")
                if updates:
                    unit.save(update_fields=updates)


def reverse_seed_automotive_unit_catalog(apps, schema_editor):
    # Keep the migration reversible without deleting records an administrator
    # may have edited or linked to products after the seed ran.
    return None


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0030_unit_management_fields_and_protection"),
    ]

    operations = [
        migrations.RunPython(
            seed_automotive_unit_catalog,
            reverse_seed_automotive_unit_catalog,
        ),
    ]
