# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20160321_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='icon',
            field=models.ImageField(upload_to=b'images/badges', blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='profile_picture',
            field=models.ImageField(default=b'/media/images/default.jpg', upload_to=b'images/profile_pictures'),
        ),
    ]
