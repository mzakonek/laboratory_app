# Generated by Django 3.0.4 on 2020-03-24 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameter',
            name='result',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='finished_at',
        ),
    ]
