# Generated by Django 4.0.6 on 2022-07-23 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0004_csvdata_csvdata_statistics__type_de87e8_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvdata',
            old_name='errors_count',
            new_name='_errors_count',
        ),
        migrations.RenameField(
            model_name='csvdata',
            old_name='info_count',
            new_name='_info_count',
        ),
    ]
