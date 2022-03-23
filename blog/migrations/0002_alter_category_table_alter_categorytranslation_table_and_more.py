# Generated by Django 4.0.3 on 2022-03-23 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='categories',
        ),
        migrations.AlterModelTable(
            name='categorytranslation',
            table='categories_translation',
        ),
        migrations.AlterModelTable(
            name='post',
            table='posts',
        ),
        migrations.AlterModelTable(
            name='postauthor',
            table='authors',
        ),
        migrations.AlterModelTable(
            name='postcomment',
            table='post_comments',
        ),
        migrations.AlterModelTable(
            name='posttranslation',
            table='posts_translation',
        ),
    ]