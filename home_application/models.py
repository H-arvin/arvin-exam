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


class Hosts(models.Model):
    ip_address = models.CharField(max_length=100)
    cloud_id = models.IntegerField(default=0)
    biz_id = models.IntegerField(default=0)
    biz_name = models.CharField(max_length=100)
    os_name = models.CharField(max_length=200)
    cloud_name = models.CharField(max_length=100)
    is_delet = models.BooleanField(default=False)
    job_id = models.IntegerField(default=0)
    host_name = models.CharField(max_length=200)
    remark = models.BooleanField(default=False)

    def toDic(self):
        temp_dic = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return temp_dic


class MonitorDetail(models.Model):
    host = models.ForeignKey(Hosts)
    load_avg = models.FloatField(default=0)
    mem_usage = models.FloatField(default=0)
    mem_free = models.FloatField(default=0)
    disk_info = models.TextField(default='')
    when_created = models.CharField(max_length=30)
    job_id = models.IntegerField(default=0)