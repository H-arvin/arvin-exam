# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from common.log import logger
from home_application.models import *
import requests
import json
import base64


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


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


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@periodic_task(run_every=crontab(minute='*', hour='*', day_of_week="*"))
def collect_host_info():
    logger.error('start task')
    host = Hosts.objects.filter(is_delet=False)
    script_content = """#!/bin/bash
    cat /proc/loadavg |awk '{print $1}'
    free -m |grep Mem |awk '{print $3,$4}'
    df -h |grep -v File
    """
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_biz_id": '',
        "bk_username": 'admin',
        "script_content": base64.b64encode(script_content),
        "ip_list": '',
        "script_type": 1,
        "account": 'root',
        "script_param": base64.b64encode(''),
    }
    url = BK_PAAS_HOST + '/api/c/compapi/v2/job/fast_execute_script/'
    for i in host:
        kwargs["bk_biz_id"] = i.biz_id
        kwargs["ip_list"] = [{"ip": i.ip_address, "bk_cloud_id": i.cloud_id}]
        res = requests.post(url, json=kwargs, verify=False)
        if res.status_code == 200:
            data = json.loads(res.content)
            job_id = data['data']['job_instance_id']
            Hosts.objects.filter(biz_id=i.biz_id, ip_address=i.ip_address, cloud_id=i.cloud_id).update(
                job_id=job_id)
            time_now = datetime.datetime.now()
            MonitorDetail.objects.create(host_id=i.id, job_id=job_id, when_created=str(time_now).split(".")[0])
            logger.error('start task success')


@periodic_task(run_every=crontab(minute='*', hour='*', day_of_week="*"))
def get_monitor_data_task():
    # logger.error('start get log')
    tasks = MonitorDetail.objects.filter(mem_usage=0)
    for i in tasks:
        # logger.error('-------------')
        # logger.error(i.host.biz_id)
        # logger.error(i.job_id)
        log_data = get_info_by_jobid(i.host.biz_id, i.job_id)
        # logger.error(log_data)
        if log_data['result']:
            logger.error('start get log success')
            dic = format_log_content(log_data['data']['log_content'])
            i.load_avg = dic['load_avg']
            i.mem_usage = dic['mem_usage']
            i.mem_free = dic['mem_free']
            i.disk_info = dic['disk_info']
            i.save()


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
            log = content['data'][0]['step_results'][0]['ip_logs'][0]
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
