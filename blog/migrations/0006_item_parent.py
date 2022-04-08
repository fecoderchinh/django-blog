# Generated by Django 4.0.3 on 2022-04-01 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_menu_alter_post_post_date_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='blog.item'),
        ),
    ]
