# Generated by Django 3.2.9 on 2022-07-12 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='user',
        ),
    ]