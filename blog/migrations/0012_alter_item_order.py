# Generated by Django 4.0.3 on 2022-04-06 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_item_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='order',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
