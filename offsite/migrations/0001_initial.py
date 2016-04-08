# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import offsite.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=offsite.models.get_upload_path_ads)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('link', models.CharField(blank=True, null=True, max_length=200)),
                ('price', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('is_payed', models.CharField(default='N', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Adser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('balance', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('customuser', models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('filter_link', models.ManyToManyField(to='offsite.Filter', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)),
                ('type', models.PositiveSmallIntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('filter_link', models.ManyToManyField(to='offsite.Filter')),
                ('object_link', models.ManyToManyField(to='offsite.Object')),
            ],
        ),
        migrations.CreateModel(
            name='Ovenbird',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('telephone', models.CharField(blank=True, null=True, max_length=13)),
                ('text', models.TextField(blank=True, null=True)),
                ('city', models.ForeignKey(null=True, blank=True, to='offsite.City')),
                ('customuser', models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=offsite.models.get_upload_path)),
                ('object', models.ManyToManyField(to='offsite.Object')),
                ('ovenbird', models.ForeignKey(to='offsite.Ovenbird')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('embed', models.CharField(max_length=255)),
                ('object', models.ForeignKey(to='offsite.Object')),
                ('ovenbird', models.ForeignKey(to='offsite.Ovenbird')),
            ],
        ),
        migrations.AddField(
            model_name='ovenbird',
            name='main_photo',
            field=models.ForeignKey(null=True, blank=True, to='offsite.Photo', related_name='main_photo', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='object',
            name='ovenbird',
            field=models.ForeignKey(to='offsite.Ovenbird'),
        ),
        migrations.AddField(
            model_name='object',
            name='title_photo',
            field=models.ForeignKey(null=True, blank=True, to='offsite.Photo', related_name='title_photo', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(to='offsite.Region'),
        ),
        migrations.AddField(
            model_name='ads',
            name='adser',
            field=models.ForeignKey(to='offsite.Adser'),
        ),
        migrations.AddField(
            model_name='ads',
            name='filter_link',
            field=models.ManyToManyField(to='offsite.Filter'),
        ),
    ]
