# Generated by Django 4.1 on 2022-08-29 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='room',
        ),
    ]
