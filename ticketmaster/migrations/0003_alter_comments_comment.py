# Generated by Django 4.2.7 on 2023-12-07 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketmaster', '0002_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(),
        ),
    ]
