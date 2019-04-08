# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExecuteJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biz_id', models.IntegerField()),
                ('biz_name', models.CharField(max_length=50)),
                ('execute_user', models.CharField(max_length=50)),
                ('exectue_time', models.CharField(max_length=100)),
                ('ip_list', models.CharField(max_length=500)),
                ('ip_log', models.TextField(default=b'')),
                ('job_id', models.IntegerField()),
                ('job_status', models.CharField(default=b'\xe6\x89\xa7\xe8\xa1\x8c\xe4\xb8\xad', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=100)),
                ('cloud_id', models.IntegerField(default=0)),
                ('app_id', models.IntegerField(default=0)),
                ('os_name', models.CharField(max_length=200)),
                ('cloud_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(default=b'', max_length=100)),
                ('when_created', models.CharField(max_length=30)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MonitorDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpu_usage', models.FloatField()),
                ('mem_usage', models.FloatField()),
                ('disk_usage', models.FloatField()),
                ('when_created', models.CharField(max_length=30)),
                ('server', models.ForeignKey(to='home_application.Host')),
            ],
        ),
    ]
