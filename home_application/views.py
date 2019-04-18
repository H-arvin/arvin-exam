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


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/js_factory.html')


def get_biz_list(request):
    """
    获取业务
    :param request:
    :return:
    """
    client = get_client_by_request(request)
    result = get_business_by_user(client, request.user.username)
    return render_json(result)


def get_cluster_list(request):
    """
    获取集群
    :param request:
    :return:
    """
    filter_obj = json.loads(request.body)
    client = get_client_by_request(request)
    result = get_cluster_by_user(client, request.user.username, filter_obj['biz_id'])
    return render_json(result)


def search_host_by_set(request):
    """
    获取主机
    :param request:
    :return:
    """
    filter_obj = json.loads(request.body)
    client = get_client_by_request(request)
    result = get_host_by_condition(client, request.user.username, filter_obj)
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
            "biz_id": filter_obj['biz_id'],
        }
        return_data.append(one_obj)
    return render_json({"result": True, "data": return_data})


def execute_job_host(request):
    """
    执行作业
    :param request:
    :return:
    """
    hosts = json.loads(request.body)
    ip_list = []
    for i in hosts:
        ip_list.append({"ip": i['ip_address'], "bk_cloud_id": i["cloud_id"]})
    client = get_client_by_request(request)
    check_obj = {'app_id': hosts[0]['biz_id'], 'ip_list': ip_list}
    script = """
    #!/bin/bash
    MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
    DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
    CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
    echo -e "$MEMORY|$DISK|$CPU"
    """
    result = fast_execute_script(check_obj, client, request.user.username, 'root', script)
    biz = get_business_by_user(client, request.user.username)
    for i in biz['data']:
        if check_obj['app_id'] == i['bk_biz_id']:
            check_obj['biz_name'] = i['bk_biz_name']
    if result['result']:
        date_now = datetime.datetime.now()
        dic = {"biz_id": check_obj['app_id'], "biz_name": check_obj['biz_name'], "execute_user": request.user.username,
               "exectue_time": str(date_now).split(".")[0], "job_id": result['data'], "ip_list": ip_list}
        ExecuteJob.objects.create(**dic)
    now = datetime.datetime.now()
    async_task.apply_async(args=[client], eta=now + datetime.timedelta(seconds=60))
    return render_json({'result': True})


def get_job(request):
    jobs = ExecuteJob.objects.all()
    data = [i.toDic() for i in jobs]
    return render_json({"result": True, "data": data})


def filter_log(request):
    filter_obj = json.loads(request.body)
    if filter_obj['biz_id']:
        jobs = ExecuteJob.objects.filter(biz_id=filter_obj['biz_id'], exectue_time__contains=filter_obj['time'])
    else:
        jobs = ExecuteJob.objects.filter(exectue_time__contains=filter_obj['time'])
    data = [i.toDic() for i in jobs]
    return render_json({"result": True, "data": data})


# arvintest

# 测试接口
def api_test(request):
    return render_json({"result": True, "data": request.user.username})


def get_all_host(request):
    filter_obj = json.loads(request.body)
    if filter_obj["ip"]:
        ip_list = filter_obj["ip"].slipt(",")
    else:
        ip_list = []
    result = search_host_by_ip(ip_list)
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
            "biz_id": filter_obj['biz_id'],
        }
        return_data.append(one_obj)
    return render_json({"result": True, "data": return_data})


COMMON_PARAMS = {
    "bk_app_code": APP_ID,
    "bk_app_secret": APP_TOKEN,
    "bk_username": "admin",
}


# def get_host_list(ip):
#     host_result = search_host()
#     if host_result["result"]:
#         if host_result["data"]["count"] == 1:
#             host_id = host_result["data"]["info"][0]["host"]["bk_host_id"]
#         elif host_result["data"]["count"] == 0:
#             host_id = ""
#         else:
#             detail = u"查询主机【{0}】失败，失败原因:主机IP地址不唯一".format(ip)
#     else:
#         detail = u"查询主机【{0}】失败，失败原因:".format(ip, host_result["message"])
#     return host_id


# 查询主机
def search_host_by_ip(ip_list):
    kwarge = {
        "bk_supplier_account": 0,
        "ip": {
            "data": ip_list,
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        }
    }
    params = dict(COMMON_PARAMS, **kwarge)
    change = "/api/c/compapi/v2/cc/search_host/"
    url = BK_PAAS_HOST + change
    # url = "http://aospaas.travelsky.com" + change
    try:
        create_result = requests.post(url, json=params, verify=False)
        return json.loads(create_result.content)
    except Exception, e:
        return {"result": False, "message": e.message}
