# Generated by Django 3.1 on 2020-11-21 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0005_auto_20201121_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitecontent',
            name='sorting',
            field=models.CharField(choices=[('default', 'Без изменений'), ('default-reverse', 'Перевернутое'), ('random', 'Случайная сортировка')], default='default', max_length=20, verbose_name='Сортировка'),
        ),
    ]
