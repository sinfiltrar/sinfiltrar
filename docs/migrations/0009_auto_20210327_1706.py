# Generated by Django 3.1.7 on 2021-03-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0008_auto_20210327_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
