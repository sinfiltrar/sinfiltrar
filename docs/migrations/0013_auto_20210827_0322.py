# Generated by Django 3.1.7 on 2021-08-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0012_auto_20210825_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='slug',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
