# Generated by Django 3.2.9 on 2022-02-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_listing_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=8, null=True),
        ),
    ]
