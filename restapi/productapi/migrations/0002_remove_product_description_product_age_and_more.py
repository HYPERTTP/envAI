# Generated by Django 4.0.5 on 2022-06-15 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='age',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=500),
        ),
    ]
