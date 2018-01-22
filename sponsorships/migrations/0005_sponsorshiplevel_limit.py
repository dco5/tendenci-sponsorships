# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0004_auto_20180110_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorshiplevel',
            name='limit',
            field=models.IntegerField(default=1),
        ),
    ]
