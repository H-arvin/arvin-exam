# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

from django.db import models


class ExecuteJob(models.Model):
    biz_id = models.IntegerField()
    biz_name = models.CharField(max_length=50)
    execute_user = models.CharField(max_length=50)
    exectue_time = models.CharField(max_length=100)
    ip_list = models.CharField(max_length=500)
    ip_log = models.TextField(default='')
    job_id = models.IntegerField()
    job_status = models.CharField(max_length=50, default='执行中')

    def toDic(self):
        temp_dic = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return temp_dic


class Host(models.Model):
    ip_address = models.CharField(max_length=100)
    cloud_id = models.IntegerField(default=0)
    app_id = models.IntegerField(default=0)
    os_name = models.CharField(max_length=200)
    cloud_name = models.CharField(max_length=100)
    created_by = models.CharField(default="", max_length=100)
    when_created = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)

    def toDic(self):
        temp_dic = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return temp_dic


class MonitorDetail(models.Model):
    server = models.ForeignKey(Host)
    cpu_usage = models.FloatField()
    mem_usage = models.FloatField()
    disk_usage = models.TextField()
    when_created = models.CharField(max_length=30)
