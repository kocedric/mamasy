# Generated by Django 3.2.5 on 2021-07-15 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='address',
            name='postcode',
        ),
    ]