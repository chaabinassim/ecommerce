# Generated by Django 4.2.2 on 2023-06-22 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='slug',
            field=models.SlugField(blank=True, max_length=128, null=True),
        ),
    ]
