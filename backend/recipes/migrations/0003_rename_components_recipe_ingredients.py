# Generated by Django 3.2.8 on 2022-08-20 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='components',
            new_name='ingredients',
        ),
    ]
