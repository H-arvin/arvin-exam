# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_auto_20190109_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='hosts',
            name='remark',
            field=models.BooleanField(default=False),
        ),
    ]
