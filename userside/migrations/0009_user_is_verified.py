# Generated by Django 4.2.5 on 2023-09-26 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0008_user_livephoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
