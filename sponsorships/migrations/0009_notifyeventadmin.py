# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0008_auto_20180309_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyEventAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notify_emails', models.CharField(max_length=250)),
                ('event', models.ForeignKey(related_name='sponsor_levels', to='events.Event')),
            ],
        ),
    ]
