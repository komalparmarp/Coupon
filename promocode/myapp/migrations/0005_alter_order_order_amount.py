# Generated by Django 4.0.1 on 2022-01-13 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_order_coupon_alter_order_order_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_amount',
            field=models.PositiveIntegerField(),
        ),
    ]
