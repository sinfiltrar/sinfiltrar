# Generated by Django 3.1.7 on 2021-09-01 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0014_auto_20210901_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
