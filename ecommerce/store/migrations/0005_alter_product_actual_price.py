# Generated by Django 4.1.2 on 2022-11-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_actual_price_product_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='actual_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]