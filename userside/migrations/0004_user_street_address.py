# Generated by Django 4.2.4 on 2023-09-13 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0003_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='street_address',
            field=models.CharField(default='', max_length=500),
        ),
    ]