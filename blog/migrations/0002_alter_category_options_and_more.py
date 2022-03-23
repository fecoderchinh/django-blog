# Generated by Django 4.0.3 on 2022-03-23 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='categorytranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Category Translation'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-post_date'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='postauthor',
            options={'ordering': ['user', 'bio'], 'verbose_name': 'Post Author', 'verbose_name_plural': 'Post Authors'},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['post_date'], 'verbose_name': 'Post Comment', 'verbose_name_plural': 'Post Comments'},
        ),
        migrations.AlterModelOptions(
            name='posttranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Post Translation'},
        ),
    ]