var app = angular.module("myApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService', 'cwLeftMenu', 'ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider", function ($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
    $urlRouterProvider.otherwise("/monitor_host");//默认展示页面
    $stateProvider.state('home', {
        url: "/home",
        controller: "home",
        templateUrl: static_url + "client/views/home.html"
    })
        .state('monitor_host', {
            url: "/monitor_host",
            controller: "monitor_host",
            templateUrl: static_url + "client/views/monitor/monitor_host.html"
        })
        .state('monitor_detail', {
            url: "/monitor_detail",
            controller: "monitor_detail",
            templateUrl: static_url + "client/views/monitor/monitor_detail.html"
        })
        .state('hostadd', {
            url: "/hostadd",
            controller: "hostadd",
            templateUrl: static_url + "client/views/monitor/hostadd.html"
        })
        .state('common_model', {
            url: "/common_model",
            controller: "common_model",
            templateUrl: static_url + "client/views/monitor/common_model.html"
        })
        .state('chart_demo', {
            url: "/chart_demo",
            controller: "chart_demo",
            templateUrl: static_url + "client/views/monitor/chart_demo.html"
        })
    ;


    // 路由配置结束

    $httpProvider.interceptors.push('authHttpResponseInterceptor');
}]).factory('authHttpResponseInterceptor', ['$q', function ($q) {
    return {
        responseError: function (rejection) {
            if (rejection.status === 500) {
                alert('服务器未知异常, 请截图并联系管理员！');
            }
            if (rejection.status === 403) {
                alert('权限不足, 请联系管理员！');
            }
            return $q.reject(rejection);
        }
    }
}]);