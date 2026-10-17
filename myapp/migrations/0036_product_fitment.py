from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0035_product_vehicle_year"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductFitment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vehicle_make", models.CharField(max_length=120)),
                ("vehicle_model", models.CharField(max_length=160)),
                (
                    "year_from",
                    models.PositiveIntegerField(
                        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
                    ),
                ),
                (
                    "year_to",
                    models.PositiveIntegerField(
                        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fitments",
                        to="myapp.product",
                    ),
                ),
            ],
            options={
                "ordering": ("vehicle_make", "vehicle_model", "year_from", "id"),
                "constraints": [
                    models.UniqueConstraint(
                        fields=(
                            "product",
                            "vehicle_make",
                            "vehicle_model",
                            "year_from",
                            "year_to",
                        ),
                        name="myapp_product_fitment_unique_range",
                    )
                ],
            },
        ),
    ]
