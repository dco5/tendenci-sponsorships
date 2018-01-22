# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0005_sponsorshiplevel_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsorship',
            name='event',
            field=models.ForeignKey(related_name='sponsorships', blank=True, to='events.Event', null=True),
        ),
    ]
