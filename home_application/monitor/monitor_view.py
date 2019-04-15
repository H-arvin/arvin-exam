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

from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from home_application.bkcommon.esb_helper import *
from home_application.celery_tasks import *
from home_application.models import *
import datetime
import json


def test(request):
    return render_json({"result": True, "message": "success", "data": request.user.username})


def arvin_test(request):
    type_obj = Hosts.objects.all().values('is_delet', 'remark').distinct()
    obj = {"app_id": 2,
           "ip_list": [{"ip": "192.168.102.227", "bk_cloud_id": 0},
                       {"ip": "192.168.102.226", "bk_cloud_id": 0},
                       {"ip": "192.168.102.194", "bk_cloud_id": 0}]}
    # client = get_client_by_request(request)
    client = get_client_by_user('admin')
    result = fast_execute_script(obj, client, 'admin', 'root', 'ifconfig')
    if result['result']:
        job_id = result['data']
        log = get_task_ip_log(client, 2, job_id, 'admin')
    return render_json({'result': True, 'data': 'aaaa'})


def get_biz_list(request):
    """
    获取业务
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    result = get_business_by_user(client, request.user.username)
    return render_json(result)


def search_host_by_biz(request):
    biz_obj = json.loads(request.body)
    client = get_client_by_request(request)
    result = search_host(client, biz_obj)
    if not result["result"]:
        return render_json({"result": False, "data": []})
    return_data = []
    for i in result["data"]["info"]:
        if i["host"]["bk_os_type"] != "1":
            continue
        one_obj = {
            "ip_address": i["host"]["bk_host_innerip"],
            "host_name": i["host"]["bk_host_name"],
            "os_name": i["host"]["bk_os_name"],
            "cloud_name": i["host"]["bk_cloud_id"][0]["bk_inst_name"],
            "cloud_id": i["host"]["bk_cloud_id"][0]["bk_inst_id"],
            "biz_id": i["biz"][0]["bk_biz_id"],
            "biz_name": i["biz"][0]["bk_biz_name"],
        }
        return_data.append(one_obj)

    return render_json({"result": True, "data": return_data})


def search_monitor_host(request):
    filter_obj = json.loads(request.body)
    if filter_obj['biz_id']:
        hosts = Hosts.objects.filter(biz_id=filter_obj['biz_id'], ip_address__contains=filter_obj['ip'], is_delet=False)
    else:
        hosts = Hosts.objects.filter(ip_address__contains=filter_obj['ip'], is_delet=False)
    return_data = [i.toDic() for i in hosts]
    return render_json({'resutl': True, 'data': return_data})


def get_all_monitor_host(requests):
    hosts = Hosts.objects.filter(is_delet=False)
    return_data = [i.toDic() for i in hosts]
    return render_json({'resutl': True, 'data': return_data})


def search_host(client, filter_obj):
    kwargs = {
        "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                # 根据业务ID查询主机
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": filter_obj["biz_id"]
                    }
                ]
            }
        ]
    }
    if filter_obj["ip"].strip():
        kwargs["ip"] = {
            "flag": "bk_host_innerip|bk_host_outerip",
            "exact": 1,
            "data": filter_obj["ip"].strip().split("\n")
        }
    result = client.cc.search_host(kwargs)
    return result


def add_host_monitor(request):
    try:
        host_obj = json.loads(request.body)
        for obj in host_obj:
            host = Hosts.objects.filter(biz_id=obj['biz_id'], ip_address=obj['ip_address'], cloud_id=obj['cloud_id'])
            if not host:

                Hosts.objects.create(**obj)
            else:
                for i in host:
                    i.is_delet = False
                    i.save()
        return render_json({'result': True, 'data': ''})
    except Exception, e:
        return render_json({'result': False, 'message': e.message})


def rm_host_monitor(request):
    obj = json.loads(request.body)['host']
    Hosts.objects.filter(biz_id=obj['biz_id'], ip_address=obj['ip_address'], cloud_id=obj['cloud_id']).update(
        is_delet=True)
    return render_json({'result': True, 'data': ''})


def get_monitor_detail(request):
    try:
        obj = json.loads(request.body)
        Hosts.objects.filter(remark=True).update(remark=False)
        host = Hosts.objects.get(biz_id=obj['biz_id'], ip_address=obj['ip_address'], cloud_id=obj['cloud_id'])
        host.remark = True
        host.save()
    except:
        host = Hosts.objects.get(remark=1)
    try:
        detail = MonitorDetail.objects.filter(mem_usage__gt=0, host=host).last()
        mem = {"used": detail.mem_usage, "unuse": detail.mem_free}
        disk = eval(detail.disk_info)
        disk_info = []
        for i in disk[1:]:
            data = i.strip().split()
            disk_obj = {
                'file_sys': data[0],
                'capacity': data[1],
                'used': data[2],
                'un_use': data[3],
                'usage_rate': data[4],
                'mount_on': data[5],
            }
            disk_info.append(disk_obj)
        load_avg = {'x': [], 'y': []}
        date_now = datetime.datetime.now() + datetime.timedelta(hours=-1)
        details = MonitorDetail.objects.filter(mem_usage__gt=0, host=host,
                                               when_created__gt=str(date_now).split(".")[0]).order_by('id')
        for i in details:
            load_avg['x'].append(i.when_created)
            load_avg['y'].append(i.load_avg)
        return render_json({'result': True, 'mem': mem, 'disk_info': disk_info, 'load_avg': load_avg})
    except Exception, e:
        return render_json({'result': False, 'message': e.message})
