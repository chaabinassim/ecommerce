# Generated by Django 4.2.2 on 2023-07-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_on_time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
