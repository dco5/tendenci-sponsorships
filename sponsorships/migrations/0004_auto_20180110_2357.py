# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20180110_2357'),
        ('sponsorships', '0003_sponsorship_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorshipLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('event', models.ForeignKey(related_name='sponsorship_levels', to='events.Event')),
            ],
            options={
                'verbose_name': 'Sponsorship Level',
                'verbose_name_plural': 'Sponsorship Levels',
            },
        ),
        migrations.AddField(
            model_name='sponsorship',
            name='level',
            field=models.ForeignKey(related_name='sponsorships', blank=True, to='sponsorships.SponsorshipLevel', null=True),
        ),
    ]
