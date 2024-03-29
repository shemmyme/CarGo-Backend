# Generated by Django 4.2.5 on 2023-11-03 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminside', '0009_alter_coupons_uses_remaining'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupons',
            name='max_uses',
        ),
        migrations.AddField(
            model_name='coupons',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cars',
            name='image_1',
            field=models.ImageField(upload_to='samples'),
        ),
        migrations.AlterField(
            model_name='cars',
            name='image_2',
            field=models.ImageField(blank=True, upload_to='samples'),
        ),
        migrations.AlterField(
            model_name='cars',
            name='image_3',
            field=models.ImageField(blank=True, upload_to='samples'),
        ),
    ]
