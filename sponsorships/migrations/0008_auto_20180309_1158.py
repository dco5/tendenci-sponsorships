# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0007_auto_20180309_1137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsorshiplevel',
            old_name='amount',
            new_name='fix_amount',
        ),
    ]
