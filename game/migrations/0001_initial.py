# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Badge 1', max_length=128)),
                ('description', models.CharField(default=b'Badge 1', max_length=128)),
                ('criteria', models.IntegerField(default=25)),
                ('badge_type', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('icon', models.ImageField(upload_to=b'icon_images', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('games_played', models.IntegerField(default=0)),
                ('most_days_survived', models.IntegerField(default=0)),
                ('most_kills', models.IntegerField(default=0)),
                ('most_people', models.IntegerField(default=1)),
                ('current_game', models.SlugField(default=b'', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
