# Generated by Django 3.1.4 on 2020-12-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201203_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_view',
            field=models.IntegerField(default=0),
        ),
    ]