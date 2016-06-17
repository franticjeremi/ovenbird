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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=offsite.models.get_upload_path_ads)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('is_payed', models.BooleanField(default=False)),
                ('auto_payment', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Реклама',
                'verbose_name': 'Реклама',
            },
        ),
        migrations.CreateModel(
            name='Adser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('customuser', models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Рекламодатели',
                'verbose_name': 'Рекламодатель',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('filter_link', models.ForeignKey(to='offsite.Filter', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Фильтры',
                'verbose_name': 'Фильтр',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('sub_location', models.ForeignKey(to='offsite.Location')),
            ],
            options={
                'verbose_name_plural': 'Локации',
                'verbose_name': 'Локация',
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('price', models.DecimalField(max_digits=10, blank=True, decimal_places=2, null=True)),
                ('type', models.PositiveSmallIntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('filter_link', models.ManyToManyField(to='offsite.Filter')),
            ],
            options={
                'verbose_name_plural': 'Объекты/Статьи',
                'verbose_name': 'Объект/Статья',
            },
        ),
        migrations.CreateModel(
            name='Ovenbird',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('telephone', models.CharField(blank=True, max_length=13, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('customuser', models.OneToOneField(default=0, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='offsite.Location', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Печники',
                'verbose_name': 'Печник',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=offsite.models.get_upload_path)),
                ('object', models.ManyToManyField(to='offsite.Object')),
                ('ovenbird', models.ForeignKey(to='offsite.Ovenbird')),
            ],
            options={
                'verbose_name_plural': 'Фотографии',
                'verbose_name': 'Фотография',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
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
            field=models.ForeignKey(to='offsite.Photo', on_delete=django.db.models.deletion.SET_NULL, related_name='main_photo', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='object',
            name='ovenbird',
            field=models.ForeignKey(to='offsite.Ovenbird'),
        ),
        migrations.AddField(
            model_name='object',
            name='title_photo',
            field=models.ForeignKey(to='offsite.Photo', on_delete=django.db.models.deletion.SET_NULL, related_name='title_photo', blank=True, null=True),
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
