# Generated by Django 3.0.4 on 2020-03-24 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('orders', '0002_auto_20200323_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='cart.Cart'),
        ),
    ]
