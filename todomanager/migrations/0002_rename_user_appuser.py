# Generated by Django 4.0.2 on 2022-02-21 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todomanager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='AppUser',
        ),
    ]
