# Generated by Django 3.1 on 2020-11-21 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0006_auto_20201121_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_online',
        ),
    ]
