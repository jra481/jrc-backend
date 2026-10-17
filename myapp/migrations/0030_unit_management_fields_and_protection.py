from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0029_product_optional_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="unittype",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="unit",
            name="symbol",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AddField(
            model_name="unit",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="unit",
            name="unit_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="units",
                to="myapp.unittype",
            ),
        ),
        migrations.AlterField(
            model_name="productvariantunit",
            name="unit_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="myapp.unittype",
                verbose_name="Unit (e.g. GB/KG)",
            ),
        ),
        migrations.AlterField(
            model_name="productvariantunit",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="myapp.unit",
                verbose_name="Quantity (e.g. 128, 1)",
            ),
        ),
    ]
