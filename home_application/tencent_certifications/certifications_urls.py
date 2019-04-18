# -*- coding:utf-8 -*-
"""
@AUTHER: arvin
@IDE: PyCharm
@TIME: 2019-04-17 22:33
@MAIL: arvin@canway.net
@PHONE: 18823412169
"""
from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.tencent_certifications.certifications_view',
    (r'^api/test$', 'test')
)