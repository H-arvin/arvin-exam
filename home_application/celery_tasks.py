# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
import datetime
import time
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from common.log import logger
from home_application.models import *
import requests
import json
import base64
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from home_application.bkcommon.esb_helper import *


@task()
def async_task(client):
    """
    定义一个 celery 异步任务
    """
    logger.error('开始')
    jobs = ExecuteJob.objects.all()
    for i in jobs:
        one_app_result = get_task_ip_log(client, 11, i.job_id, 'huangxiaojian')
        logger.error(one_app_result)
        i.ip_log = one_app_result[0]["log_content"]
        i.job_status = 'success'
        i.save()


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    return ''


def get_info_by_jobid(biz_id, job_id):
    url = BK_PAAS_HOST + '/api/c/compapi/v2/job/get_job_instance_log/'
    user = 'admin'
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": user,
        "bk_biz_id": biz_id,
        "job_instance_id": job_id
    }
    res = requests.get(url, params=kwargs, verify=False)
    content = json.loads(res.content)
    if content['result']:
        if content['data'][0]['step_results'][0]['ip_status'] == 9:
            log = content['data'][0]['step_results'][0]['ip_logs']
            return {'result': True, 'data': log}
        return {'result': False, 'message': content['data'][0]['step_results'][0]['ip_logs'][0]}
    return {'result': False, 'message': content['message']}


def format_log_content(log_content):
    log_result = log_content.strip().split("\n")
    logger.error(u'日志清洗')
    logger.error(log_result)
    logger.error(u'日志清洗结束')
    one_obj = {
        "load_avg": log_result[0],
        "mem_usage": log_result[1].split(' ')[0],
        "mem_free": log_result[1].split(' ')[1],
        "disk_info": log_result[2:],
    }
    return one_obj


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_monitor_detail():
    logger.error('开始')
    hosts = Host.objects.filter(is_deleted=False)
    host_list = [i.toDic() for i in hosts]
    ip_dic = {}
    for host in host_list:
        if host["app_id"] in ip_dic.keys():
            ip_dic[host["app_id"]].append({"ip": host['ip_address'], "bk_cloud_id": host["cloud_id"]})
        else:
            ip_dic[host["app_id"]] = []
            ip_dic[host["app_id"]].append({"ip": host['ip_address'], "bk_cloud_id": host["cloud_id"]})

    client = get_client_by_user("admin")
    script = """
    #!/bin/bash
    MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
    DISK=$(df -h)
    CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
    echo -e "$MEMORY|$CPU|$DISK"
    """
    for biz_id in ip_dic.keys():
        check_obj = {'app_id': biz_id, 'ip_list': ip_dic[biz_id]}
        result = fast_execute_script(check_obj, client, "admin", 'root', script)
        if result["result"]:
            time.sleep(5)
            detail = get_info_by_jobid(biz_id, result["data"])
            logger.error(detail)
            if detail["result"]:
                sync_detail(detail["data"])


def sync_detail(log_list):
    for i in log_list:
        host = Host.objects.get(ip_address=i["ip"])
        detail = i["log_content"].split("|")
        date_now = datetime.datetime.now()
        MonitorDetail.objects.create(mem_usage=detail[0][:3], cpu_usage=detail[1][:3], disk_usage=detail[2],
                                     server=host,
                                     when_created=str(date_now).split(".")[0])


# if __name__ == "__main__":
#     get_monitor_detail()
#     print "a"
