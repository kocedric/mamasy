# Generated by Django 3.2.5 on 2021-07-10 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='long_desc',
            field=models.TextField(blank=True, null=True, verbose_name='Description longue'),
        ),
    ]
