# Generated by Django 3.1.7 on 2021-03-23 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issuers', '0002_auto_20210323_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuer_name', models.CharField(max_length=200)),
                ('from_email', models.CharField(max_length=254)),
                ('issued_at', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('short_text', models.CharField(max_length=255)),
                ('body_html', models.TextField()),
                ('body_plain', models.TextField()),
                ('body_md', models.TextField()),
                ('media', models.JSONField()),
                ('meta', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issuers.issuer')),
            ],
        ),
    ]