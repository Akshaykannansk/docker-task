# Generated by Django 3.2.6 on 2023-03-03 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_cartitems_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
