# Generated by Django 5.1.1 on 2024-09-16 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='notes',
            field=models.TextField(max_length=512, verbose_name='notes'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='notes',
            field=models.TextField(max_length=2048, verbose_name='notes'),
        ),
    ]
