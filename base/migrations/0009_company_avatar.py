# Generated by Django 4.2.7 on 2023-12-28 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_invoice_quantity_alter_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='avatar',
            field=models.ImageField(default='avatar.svg', upload_to=''),
        ),
    ]