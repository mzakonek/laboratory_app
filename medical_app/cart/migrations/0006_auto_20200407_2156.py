# Generated by Django 3.0.4 on 2020-04-07 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_ordered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]