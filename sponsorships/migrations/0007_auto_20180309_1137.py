# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0006_auto_20180112_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorshiplevel',
            name='max_amount',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='sponsorshiplevel',
            name='min_amount',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='sponsorshiplevel',
            name='uses_fix_amount',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sponsorshiplevel',
            name='amount',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
    ]
