# Generated by Django 3.2 on 2021-04-24 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('thumbnail', models.ImageField(upload_to='uploads/')),
            ],
        ),
    ]
