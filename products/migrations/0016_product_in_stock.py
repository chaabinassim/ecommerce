# Generated by Django 4.2.2 on 2023-08-12 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_collection_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]