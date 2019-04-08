# -*- coding: utf-8 -*-
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from common.log import logger
from esb_helper import html_escape
from common.mymako import render_mako_context, render_json
from conf.default import RUN_MODE
import json
import datetime
import requests
import os


def push_script(request):
    """
    读取上传文件内容内容
    :param request:
    :return:
    """
    file = request.FILES.get('files')
    # file_name = str(file.name).decode('utf-8')
    # file_suffix = os.path.splitext(file_name)[1][1:]
    script_content = file.read()
    script_content = html_escape(script_content)
    return render_json({'result': True, 'data': script_content})


def mkdir(path):
    """
    文件上传创建路径
    :param path:
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def push_file(request):
    """
    文件分发，获取上传文件
    :param request:
    :return:
    """
    wkf_ins_id = request.GET.get('wkf_ins_id')
    file = request.FILES.get('files')
    file_name = file.name
    # raise Exception("test")
    date = datetime.datetime.now().strftime('%Y%m%d')
    logger.error('上传')
    if RUN_MODE == 'DEVELOP':
        path = 'C:\\uploadfile\\arvin_cert\\'
        mkdir(path)
        file_path = path + '\\' + file_name
    else:
        logger.error('正式环境')
        path = '/opt/bksaas/uploadfile/arvin_cert/'
        mkdir(path)
        file_path = path + '/' + file_name
        logger.error(path)
    if os.path.exists(file_path):
        os.remove(file_path)
    try:
        logger.error('读取文件')
        file_obj = open(file_path, 'wb')
        for chunk in file.chunks():
            file_obj.write(chunk)
        file_obj.close()
    except Exception, e:
        logger.error('文件保存失败，请重新上传')
        logger.error(e.message)
        raise Exception(render_json({'result': False, 'message': '文件保存失败，请重新上传'}))
    return render_json({'result': True, 'data': file_path})


def get_biz_by_user(user):
    """
    业务查询
    :param user:
    :return:
    """
    url = BK_PAAS_HOST + '/api/c/compapi/v2/cc/search_business/'
    params = {'bk_app_code': APP_ID,
              'bk_app_secret': APP_TOKEN,
              'bk_username': user,
              'fields': ['bk_biz_id', 'bk_biz_name'],
              'page': {'limit': 200, 'start': 0}}
    try:
        r = requests.post(url, json=params, verify=False)
        biz_data = json.loads(r.content)
        if biz_data['result']:
            data = biz_data['data']
            return {'result': True, 'data': data}
        else:
            message = biz_data['message']
            return {'result': False, 'message': message}
    except Exception, e:
        return {'result': False, 'message': e.message}


def search_host(biz_id, condition):
    params = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": "admin",
        "bk_biz_id": biz_id,
        "condition": condition
    }
    import json
    change = "/api/c/compapi/v2/cc/search_host"
    post_url = BK_PAAS_HOST + change
    request = requests.post(post_url, json=params, verify=False)
    data = json.loads(request.content)
    return data['data']['info']


# 根据业务获取主机
def get_host(request):
    bk_biz_id = request.POST.get('bk_biz_id')
    params = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": "admin",
        "bk_biz_id": bk_biz_id}
    change = "/api/c/compapi/v2/cc/search_host"
    post_url = BK_PAAS_HOST + change
    r = requests.post(post_url, json=params, verify=False)
    data = json.loads(r.content)
    if data['result']:
        host_list = []
        num = data['data']['count']
        for i in data['data']['info']:
            host_list.append({'hostname': i['host']['bk_host_name'],
                              'bk_os_name': i['host']['bk_os_name'],
                              'bk_host_innerip': i['host']['bk_host_innerip'],
                              'bk_cloud_name': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                              'bk_cloud_id': i['host']['bk_cloud_id'][0]['bk_inst_id']
                              })
        return render_json({'result': True, 'data': {'count': num, 'data': host_list, }})
    return render_json({'result': False, 'message': data['message']})