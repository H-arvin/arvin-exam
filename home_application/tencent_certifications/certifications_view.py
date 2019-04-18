# -*- coding:utf-8 -*-
"""
@AUTHER: arvin
@IDE: PyCharm
@TIME: 2019-04-17 22:36
@MAIL: arvin@canway.net
@PHONE: 18823412169
"""
from common.mymako import render_json


def test(request):
    return render_json({"result": True, "message": "success", "data": request.user.username})
