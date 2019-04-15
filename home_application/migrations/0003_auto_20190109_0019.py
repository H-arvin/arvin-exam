# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20190109_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitordetail',
            name='disk_info',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='monitordetail',
            name='load_avg',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='monitordetail',
            name='mem_free',
            field=models.FloatField(default=0),
        ),
    ]
