# Generated by Django 3.2.9 on 2022-02-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_listing_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='initial_bid',
            field=models.IntegerField(),
        ),
    ]
