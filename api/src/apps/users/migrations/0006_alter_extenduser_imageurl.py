# Generated by Django 3.2.15 on 2022-08-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220825_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='imageUrl',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
