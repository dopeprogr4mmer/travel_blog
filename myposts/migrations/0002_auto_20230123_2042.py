# Generated by Django 2.2 on 2023-01-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myposts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='overview',
            field=models.CharField(max_length=200),
        ),
    ]
