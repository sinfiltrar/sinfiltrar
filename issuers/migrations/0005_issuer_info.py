# Generated by Django 3.1.13 on 2021-09-01 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuers', '0004_issuer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuer',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
