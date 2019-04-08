# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^api/test$', 'api_test'),
    (r'^get_biz_list$', 'get_biz_list'),
    (r'^get_cluster_list$', 'get_cluster_list'),
    (r'^search_host_by_set$', 'search_host_by_set'),
    (r'^execute_job_host$', 'execute_job_host'),
    (r'^get_job$', 'get_job'),
    (r'^filter_log$', 'filter_log'),


    (r'^get_all_host$', 'get_all_host'),
    (r'^search_host_by_ip$', 'search_host_by_ip'),


)
