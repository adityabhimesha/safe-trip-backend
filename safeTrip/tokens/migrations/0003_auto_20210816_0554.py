# Generated by Django 3.2.6 on 2021-08-16 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0002_auto_20210815_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokens',
            name='pair_base_address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='tokens',
            name='pair_quote_address',
            field=models.CharField(default='', max_length=255),
        ),
    ]
