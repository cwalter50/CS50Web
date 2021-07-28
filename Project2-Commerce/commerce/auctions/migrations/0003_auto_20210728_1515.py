# Generated by Django 3.2.4 on 2021-07-28 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='starting_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default='NA', max_length=64),
        ),
    ]
