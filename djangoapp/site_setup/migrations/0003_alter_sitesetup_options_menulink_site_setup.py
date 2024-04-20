# Generated by Django 5.0.4 on 2024-04-19 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0002_sitesetup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesetup',
            options={'verbose_name': 'Setup', 'verbose_name_plural': 'Setup'},
        ),
        migrations.AddField(
            model_name='menulink',
            name='site_setup',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_setup.sitesetup'),
        ),
    ]