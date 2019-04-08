# -*- coding: utf-8 -*-

import base64
import time
import sys
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from common.log import logger

reload(sys)
sys.setdefaultencoding("utf8")


def fast_execute_script(check_app, client, user_name, execute_account, script_content, param_content='',
                        script_timeout=1000):
    """
    快速执行脚本
    :param check_app: 操作的对象，dict，{"app_id":1,"ip_list":[{"ip":"10.0.0.10","bk_cloud_id":0}]}
    :param client: ESB连接客户端，client class
    :param user_name:  有该业务操作权限的用户，str
    :param execute_account: 脚本执行帐号，str
    :param script_content: 脚本执行内容，str
    :param param_content: 脚本参数，str，可不传
    :param script_timeout: 超时时间，int，可不传
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_biz_id": check_app["app_id"],
        "bk_username": user_name,
        "script_content": base64.b64encode(script_content),
        "ip_list": check_app["ip_list"],
        "script_type": 1,
        "account": execute_account,
        "script_param": base64.b64encode(param_content),
        "script_timeout": script_timeout
    }
    result = client.job.fast_execute_script(kwargs)
    if result["result"]:
        return {"result": True, "data": result["data"]["job_instance_id"]}

    else:
        return {"result": False, "data": result["message"]}


def fast_push_file(check_app, client, user_name, execute_account, target_path, source):
    """
    快速分发文件
    :param check_app: 操作的对象，dict，{"app_id":1,"ip_list":[{"ip":"10.0.0.10","bk_cloud_id":0}]}
    :param client: ESB连接客户端，client class
    :param user_name:  有该业务操作权限的用户，str
    :param execute_account: 脚本执行帐号，str
    :param script_content: 脚本执行内容，str
    :param source: 文件对象，[{"files": ["/tmp/REGEX:[a-z]*.txt"],
                                "account": "root",
                                "ip_list": [{"bk_cloud_id": 0, "ip": "10.0.0.1"}]}]
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_biz_id": check_app["app_id"],
        "bk_username": user_name,
        "file_target_path": target_path,
        "file_source": source,
        "ip_list": check_app["ip_list"],
        "account": execute_account,
    }
    result = client.job.fast_push_file(kwargs)
    if result["result"]:
        return {"result": True, "data": result["data"]["job_instance_id"]}

    else:
        return {"result": False, "data": result["message"]}


def get_task_ip_log(client, app_id, task_instance_id, user_name, count=0):
    """
    获取脚本执行结果
    :param client: ESB连接客户端，client class
    :param app_id: 业务ID，int
    :param task_instance_id: 作业实例ID，int
    :param user_name: 有查看该脚本执行结果权限的用户 ,str
    :param count: 已重试的次数，直接调用不传
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": user_name,
        "bk_biz_id": app_id,
        "job_instance_id": int(task_instance_id)
    }
    result = client.job.get_job_instance_log(kwargs)
    if not result["result"]:
        count += 1
        if count > 5:
            logger.error(result["message"])
            return []
        time.sleep(10)
        return get_task_ip_log(client, app_id, task_instance_id, user_name, count)
    if result["data"][0]["is_finished"]:
        log_content = []
        for i in result["data"][0]["step_results"]:
            log_content += [{"ip": u["ip"], "log_content": u["log_content"], "bk_cloud_id": u["bk_cloud_id"],
                             "is_success": i['ip_status'] == 9} for u in
                            i["ip_logs"]]
        return log_content
    time.sleep(10)
    return get_task_ip_log(client, app_id, task_instance_id, user_name)


def get_business_by_user(client, username):
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username
    }
    res = client.cc.search_business(kwargs)
    if res["result"]:
        user_business_list = [
            {"bk_biz_id": i["bk_biz_id"], "bk_biz_name": i["bk_biz_name"]} for i in res["data"]["info"]
            if username in i["bk_biz_maintainer"].split(",")
            ]
        return {"result": True, "data": user_business_list}
    return {"result": False, "data": res["data"]}


def get_cluster_by_user(client, username, biz_id):
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "bk_biz_id": biz_id
    }
    res = client.cc.search_set(kwargs)
    if res['result']:
        user_cluster_list = [{"bk_biz_id": i["bk_biz_id"], "bk_set_id": i["bk_set_id"], "bk_set_name": i["bk_set_name"]}
                             for i in res["data"]["info"]]
        return {"result": True, "data": user_cluster_list}
    return {"result": False, "data": res["data"]}


def get_host_by_condition(client, username, filter_obj):
    condition = [
        {
            "bk_obj_id": "set",
            # 根据集群ID查询主机
            "condition": [
                {
                    "field": "bk_set_id",
                    "operator": "$eq",
                    "value": filter_obj["set_id"]
                }
            ]
        }
    ]
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "condition": condition
    }
    result = client.cc.search_host(kwargs)
    return result


def html_escape(html):
    """
    替换日志显示符号
    :param html:
    :return:
    """
    html = html.replace('&quot;', '"')
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&nbsp;', ' ')
    return html


a = [{"files": ["/tmp/REGEX:[a-z]*.txt"],
      "account": "root",
      "ip_list": [{"bk_cloud_id": 0, "ip": "10.0.0.1"}]}]
