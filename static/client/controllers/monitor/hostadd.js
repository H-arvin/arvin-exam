/**
 * Created by arvin on 2019-1-5 0005.
 */
controllers.controller("hostadd", ["$scope", "msgModal", "monitorService", "loading", "$modalInstance", "errorModal", function ($scope, msgModal, monitorService, loading, $modalInstance, errorModal) {
    $scope.title = '新增监控主机';
    $scope.newhost = {biz_id: "", ip: ""};

    $scope.add_host = [];
    $scope.ok = function () {
        loading.open();
        monitorService.add_host_monitor({},$scope.add_host,function (res) {
            loading.close();
            if(res.result){
                $modalInstance.close($scope.add_host);
            }else{
            }

        })

    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    $scope.biz_list = [];
    $scope.init = function () {
        loading.open();
        monitorService.get_biz_list({}, {}, function (res) {
            loading.close();
            $scope.biz_list = res.data;
        })
    };
    $scope.init();


    $scope.hostlist = [];

    $scope.searchhost = function () {
        loading.open();
        console.log();
        monitorService.search_host_by_biz({}, $scope.newhost, function (res) {
            loading.close();
            $scope.hostlist = res.data;
        })
    };

    $scope.gridOption = {
        data: 'hostlist',
        columnDefs: [
            {
                displayName: 'checked', width: 80,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<input type="checkbox" ng-click="checded_host(row.entity,$event)">' +
                '</div>'
            },
            {field: 'ip_address', displayName: '主机IP'},
            {field: 'host_name', displayName: '主机名称'},
            {field: 'cloud_name', displayName: '云区域'},
            {field: 'os_name', displayName: 'OS'}
        ]
    };

    $scope.checded_host = function (obj, event) {
        // console.log($scope.add_host);
        // console.log(event);
        var action = event.target.checked;
        console.log(action);
        if (action) {
            if ($scope.add_host.indexOf(obj)==-1) {
                $scope.add_host.push(obj);
                console.log($scope.add_host);
            }

        }
    }

}]);
