# Generated by Django 4.2.11 on 2024-05-29 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AccountsApp', '0012_useraccount_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='image',
        ),
    ]