# Generated by Django 4.2.2 on 2023-06-22 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_rename_delivery_address_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be 10 digits long and start with 05, 06, or 07.', regex='^0[567]\\d{8}$')]),
        ),
    ]