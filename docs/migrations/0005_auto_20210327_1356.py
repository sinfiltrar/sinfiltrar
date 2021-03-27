# Generated by Django 3.1.7 on 2021-03-27 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issuers', '0002_auto_20210323_1840'),
        ('docs', '0004_auto_20210327_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='issuer_email',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='issuers.issueremail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doc',
            name='from_email',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='doc',
            name='issuer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='issuers.issuer'),
        ),
    ]