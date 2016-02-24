# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import offsite.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('customuser', models.OneToOneField(to=settings.AUTH_USER_MODEL, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)),
                ('type', models.PositiveSmallIntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ovenbird',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=13, blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('city', models.ForeignKey(to='offsite.City', blank=True, null=True)),
                ('customuser', models.OneToOneField(to=settings.AUTH_USER_MODEL, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=offsite.models.get_upload_path)),
                ('object', models.ForeignKey(to='offsite.Object')),
                ('ovenbird', models.ForeignKey(to='offsite.Ovenbird')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('file', models.FileField(upload_to=offsite.models.get_upload_path)),
                ('object', models.ForeignKey(to='offsite.Object')),
                ('ovenbird', models.ForeignKey(to='offsite.Ovenbird')),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='ovenbird',
            field=models.ForeignKey(to='offsite.Ovenbird'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(to='offsite.Region'),
        ),
    ]
