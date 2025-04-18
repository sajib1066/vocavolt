# Generated by Django 4.2.20 on 2025-04-17 17:14

import customauth.models.profile
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Email Address')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Status')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active Status')),
                ('accepted_terms', models.BooleanField(default=False, verbose_name='accepted terms')),
                ('read_terms', models.BooleanField(default=False, verbose_name='terms read')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('email_token', models.CharField(blank=True, max_length=255, null=True, verbose_name='email token')),
                ('additional_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='additional email address')),
                ('verified_email', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=customauth.models.profile.avatar_upload_path)),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Bio')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
