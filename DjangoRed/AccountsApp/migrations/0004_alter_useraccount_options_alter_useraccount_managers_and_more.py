# Generated by Django 4.2.11 on 2024-05-05 16:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AccountsApp', '0003_useraccount_delete_myuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraccount',
            options={},
        ),
        migrations.AlterModelManagers(
            name='useraccount',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='username',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
