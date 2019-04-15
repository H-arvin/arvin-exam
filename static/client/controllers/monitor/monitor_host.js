/**
 * Created by arvin on 2019-1-5 0005.
 */
controllers.controller("monitor_host", ["$scope", "monitorService", "$modal", "loading", "confirmModal", "msgModal", "$location", function ($scope, monitorService, $modal, loading, confirmModal, msgModal, $location) {
    $scope.host_filter = {biz_id: '', ip: ''};
    $scope.biz_id = 0;
    $scope.biz_list = [];
    $scope.init = function () {
        loading.open();
        monitorService.get_biz_list({}, {}, function (res) {
            $scope.biz_list = res.data;
        });
        monitorService.get_all_monitor_host({}, {}, function (res) {
            $scope.host_list = res.data;
            console.log($scope.host_list)
            loading.close();
        })
    };
    $scope.init();

    $scope.host_list = [];
    $scope.gridOption = {
        data: 'host_list',
        columnDefs: [
            {field: 'ip_address', displayName: '主机IP'},
            {field: 'host_name', displayName: '主机名称'},
            {field: 'biz_name', displayName: '所属业务'},
            {field: 'cloud_name', displayName: '云区域'},
            {field: 'os_name', displayName: 'OS'},
            {field: 'remark', displayName: '备注'},
            {
                displayName: '操作', width: 180,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<span  class="fa fa-search fa-icon" title="查看性能" style="min-width:50px;margin-left: 5px;cursor:pointer;" ng-click="searchDetail(row.entity)"></span>' +
                '<span  class="fa fa-search fa-close" title="移除监控"  style="min-width:50px;margin-left: 5px;cursor:pointer;" ng-click="rmmonitor(row.entity)"></span>' +
                '</div>'
            }
        ]
    };

    $scope.searchhost = function () {
        if ($scope.host_filter.biz_id || $scope.host_filter.ip) {
            loading.open('searching');
            monitorService.search_monitor_host({}, $scope.host_filter, function (res) {
                    loading.close();
                    $scope.host_list = res.data;
                }
            )
        }else {
            msgModal.open('error','请填写筛选条件')
        }
    }
    ;

    $scope.hostadd = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/monitor/hostadd.html',
            windowClass: 'dialogApp',
            controller: 'hostadd',
            backdrop: 'static'
        });
        modalInstance.result.then(function (res) {
            console.log('bbbbb')
            $scope.init();
        });
    };

    $scope.searchDetail = function (obj) {
        $scope.return_id = $location.path().split('/')[1];
        $location.path('monitor_detail').search({host_obj: obj, return_page: $scope.return_id});
    };
    $scope.rmmonitor = function (obj) {
        loading.open();
        monitorService.rm_host_monitor({}, {host: obj}, function (res) {
            loading.close();
        });
        $scope.init();
    }
}])
;