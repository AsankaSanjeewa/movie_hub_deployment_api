# Generated by Django 4.1 on 2022-08-05 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='excerpt',
        ),
        migrations.AddField(
            model_name='books',
            name='author',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='review',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='books',
            name='year_published',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
