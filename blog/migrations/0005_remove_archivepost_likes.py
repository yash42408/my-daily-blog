# Generated by Django 2.2 on 2020-12-02 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_archivepost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivepost',
            name='likes',
        ),
    ]