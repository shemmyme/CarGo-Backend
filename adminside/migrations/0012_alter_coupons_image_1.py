# Generated by Django 4.2.5 on 2023-11-04 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0011_remove_coupons_user_usercouponusage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='image_1',
            field=models.ImageField(upload_to=''),
        ),
    ]