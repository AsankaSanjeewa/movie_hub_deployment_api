# Generated by Django 3.2.15 on 2022-08-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_extenduser_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='extenduser',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
