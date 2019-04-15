# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_auto_20190109_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitordetail',
            name='disk_info',
            field=models.TextField(default=b''),
        ),
    ]
