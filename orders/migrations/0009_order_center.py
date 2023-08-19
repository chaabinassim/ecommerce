# Generated by Django 4.2.2 on 2023-07-21 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_center'),
        ('orders', '0008_order_is_stopdesk'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.center'),
        ),
    ]