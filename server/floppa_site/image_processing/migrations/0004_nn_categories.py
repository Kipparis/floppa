# Generated by Django 3.2 on 2021-04-24 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0003_nnimage_nnimagemarkup'),
    ]

    operations = [
        migrations.AddField(
            model_name='nn',
            name='categories',
            field=models.ManyToManyField(to='image_processing.Category'),
        ),
    ]