# Generated by Django 4.1.5 on 2023-02-01 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='biding',
            options={'ordering': ['value']},
        ),
    ]
