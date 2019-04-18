services = angular.module('webApiService', ['ngResource', 'utilServices']);

//生产代码
var POST = "POST";
var GET = "GET";

//测试代码
//var sourceRoute = "./Client/MockData";
//var fileType = ".html";
//var POST = "GET";
//var GET = "GET";
services.factory('sysService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            server_search: {method: GET, params: {actionName: 'server_search'}, isArray: false},
            server_delete: {method: POST, params: {actionName: 'server_delete'}, isArray: false}
        });
}]).factory('monitorService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            get_biz_list: {method: POST, params: {actionName: 'get_biz_list'}, isArray: false},
            get_cluster_list: {method: POST, params: {actionName: 'get_cluster_list'}, isArray: false},
            search_host_by_set: {method: POST, params: {actionName: 'search_host_by_set'}, isArray: false},
            search_host_by_biz: {method: POST, params: {actionName: 'search_host_by_biz'}, isArray: false},
            add_host_monitor: {method: POST, params: {actionName: 'add_host_monitor'}, isArray: false},
            get_all_monitor_host: {method: POST, params: {actionName: 'get_all_monitor_host'}, isArray: false},
            rm_host_monitor: {method: POST, params: {actionName: 'rm_host_monitor'}, isArray: false},
            search_monitor_host: {method: POST, params: {actionName: 'search_monitor_host'}, isArray: false},
            get_monitor_detail: {method: POST, params: {actionName: 'get_monitor_detail'}, isArray: false}
        });
}]).factory('certificateService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            // get_biz_list: {method: POST, params: {actionName: 'get_biz_list'}, isArray: false},
            // get_cluster_list: {method: POST, params: {actionName: 'get_cluster_list'}, isArray: false},
            // search_host_by_set: {method: POST, params: {actionName: 'search_host_by_set'}, isArray: false},
            // execute_job_host: {method: POST, params: {actionName: 'execute_job_host'}, isArray: false},
            // get_job: {method: POST, params: {actionName: 'get_job'}, isArray: false},
            // filter_log: {method: POST, params: {actionName: 'filter_log'}, isArray: false},
        });
}]).factory('arvintest', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            search_host_by_ip: {method: POST, params: {actionName: 'search_host_by_ip'}, isArray: false},
            get_all_host: {method: POST, params: {actionName: 'get_all_host'}, isArray: false},
        });
}])


;//这是结束符，请勿删除