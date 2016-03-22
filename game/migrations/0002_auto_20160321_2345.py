# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='achievementHandler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('achievement', models.ForeignKey(related_name=b'userbadges', to='game.Badge')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='player',
            name='profile_picture',
            field=models.ImageField(upload_to=b'static/images', blank=True),
        ),
    ]
