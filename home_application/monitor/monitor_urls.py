# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.monitor.monitor_view',
    # (r'^api/test$', 'test'),
    (r'^arvin_test$', 'arvin_test'),
    (r'^get_biz_list$', 'get_biz_list'),
    (r'^search_host_by_biz$', 'search_host_by_biz'),
    (r'^get_all_monitor_host$', 'get_all_monitor_host'),
    (r'^search_monitor_host$', 'search_monitor_host'),
    (r'^add_host_monitor$', 'add_host_monitor'),
    (r'^rm_host_monitor$', 'rm_host_monitor'),
    (r'^get_monitor_detail$', 'get_monitor_detail'),
)