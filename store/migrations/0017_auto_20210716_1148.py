# Generated by Django 3.2.5 on 2021-07-16 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210715_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='additional_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='invoicing_address',
        ),
    ]
