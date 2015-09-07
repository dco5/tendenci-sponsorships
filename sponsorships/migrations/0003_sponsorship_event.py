# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0002_auto_20150906_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorship',
            name='event',
            field=models.ForeignKey(blank=True, to='events.Event', null=True),
        ),
    ]
