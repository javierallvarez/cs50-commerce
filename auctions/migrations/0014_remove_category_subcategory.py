# Generated by Django 3.2.9 on 2022-02-08 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20220205_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory',
        ),
    ]
