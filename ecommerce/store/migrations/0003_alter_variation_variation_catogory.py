# Generated by Django 4.1.2 on 2022-11-11 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_catogory',
            field=models.CharField(choices=[('size', 'size')], max_length=100),
        ),
    ]