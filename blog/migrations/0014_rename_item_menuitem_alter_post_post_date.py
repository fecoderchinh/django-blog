# Generated by Django 4.0.3 on 2022-04-07 02:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_item_order'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='MenuItem',
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateField(default=datetime.date(2022, 4, 7)),
        ),
    ]