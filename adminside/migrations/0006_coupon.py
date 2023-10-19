# Generated by Django 4.2.5 on 2023-10-16 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0005_remove_cars_rental_places_cars_rental_place_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=255, unique=True)),
                ('discount_perc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('max_uses', models.PositiveIntegerField()),
                ('uses_remaining', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
