# Generated by Django 4.2.7 on 2023-12-16 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='character',
            new_name='role',
        ),
    ]
