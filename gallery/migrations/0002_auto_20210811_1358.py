# Generated by Django 2.2 on 2021-08-11 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='data',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]