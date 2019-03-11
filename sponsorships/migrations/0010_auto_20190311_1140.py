# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20190311_1140'),
        ('sponsorships', '0009_notifyeventadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyEventSponsorshipAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notify_emails', models.CharField(max_length=250)),
                ('event', models.ForeignKey(related_name='notification_emails', to='events.Event')),
            ],
            options={
                'verbose_name': 'Sponsorship Notification Emails',
                'verbose_name_plural': 'Sponsorship Notification Emails',
            },
        ),
        migrations.RemoveField(
            model_name='notifyeventadmin',
            name='event',
        ),
        migrations.DeleteModel(
            name='NotifyEventAdmin',
        ),
    ]
