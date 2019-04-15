# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=100)),
                ('cloud_id', models.IntegerField(default=0)),
                ('biz_id', models.IntegerField(default=0)),
                ('biz_name', models.CharField(max_length=100)),
                ('os_name', models.CharField(max_length=200)),
                ('cloud_name', models.CharField(max_length=100)),
                ('is_delet', models.BooleanField(default=False)),
                ('job_id', models.IntegerField(default=0)),
                ('host_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MonitorDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('load_avg', models.FloatField()),
                ('mem_usage', models.FloatField()),
                ('mem_free', models.FloatField()),
                ('disk_info', models.TextField()),
                ('when_created', models.CharField(max_length=30)),
                ('job_id', models.IntegerField(default=0)),
                ('host', models.ForeignKey(to='home_application.Hosts')),
            ],
        ),
    ]
