# Generated by Django 4.2.2 on 2023-07-22 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_center'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_fee', models.PositiveIntegerField()),
                ('desk_fee', models.PositiveIntegerField()),
                ('wilaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.wilaya')),
            ],
        ),
    ]
