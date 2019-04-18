/**
 * Created by arvin on 2019-4-8 0008.
 */
controllers.controller("host_list", ["$scope", "arvintest", "$modal", "loading", "confirmModal", "msgModal", "$location", function ($scope, arvintest, $modal, loading, confirmModal, msgModal, $location) {
    // $scope.host_filter = {biz_id: '', set_id: ''}
    // ;
    // $scope.biz_id = 0;
    // $scope.biz_list = [];
    // $scope.init = function () {
    //     loading.open();
    //     certificateService.get_biz_list({}, {}, function (res) {
    //         $scope.biz_list = res.data;
    //         loading.close()
    //     });
    // };
    // $scope.init();
    //
    // $scope.cluster_list = [];
    // $scope.search_cluster = function (obj) {
    //     console.log($scope.host_filter);
    //     if ($scope.host_filter.biz_id) {
    //         loading.open();
    //         certificateService.get_cluster_list({}, $scope.host_filter, function (res) {
    //                 $scope.cluster_list = res.data;
    //                 loading.close()
    //             }
    //         )
    //     } else {
    //         $scope.cluster_list = []
    //     }
    //
    // }
    // ;
    //
    $scope.host_filter = {"ip":""};
    $scope.host_list = [];
    $scope.init = function () {
        loading.open();
        arvintest.get_all_host({}, $scope.host_filter, function (res) {
            $scope.host_list = res.data;
            loading.close()
        });
    };
    $scope.init();

    $scope.gridOption = {
        data: 'host_list',
        columnDefs: [
            {
                displayName: '选择', width: 80,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<input type="checkbox" ng-click="checded_host(row.entity,$event)">' +
                '</div>'
            },
            {field: 'ip_address', displayName: '主机IP'},
            {field: 'host_name', displayName: '主机名称'},
            {field: 'biz_name', displayName: '所属业务'},
            {field: 'cloud_name', displayName: '云区域'},
            {field: 'os_name', displayName: 'OS'}
            // {field: 'remark', displayName: '备注'}
            // {
            //     displayName: '操作', width: 180,
            //     cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
            //     '<span  class="fa fa-search fa-icon" title="查看性能" style="min-width:50px;margin-left: 5px;cursor:pointer;" ng-click="searchDetail(row.entity)"></span>' +
            //     '<span  class="fa fa-search fa-close" title="移除监控"  style="min-width:50px;margin-left: 5px;cursor:pointer;" ng-click="rmmonitor(row.entity)"></span>' +
            //     '</div>'
            // }
        ]
    };
    //
    // $scope.search_host = function () {
    //     if ($scope.host_filter.biz_id && $scope.host_filter.set_id) {
    //         loading.open('searching');
    //         certificateService.search_host_by_set({}, $scope.host_filter, function (res) {
    //                 loading.close();
    //                 $scope.host_list = res.data;
    //             }
    //         )
    //     } else {
    //         msgModal.open('error', '请选择业务集群')
    //     }
    // };
    //
    // $scope.execute_host = [];
    // $scope.checded_host = function (obj, event) {
    //     // console.log($scope.add_host);
    //     // console.log(event);
    //     var action = event.target.checked;
    //     console.log(action);
    //     if (action) {
    //         if ($scope.execute_host.indexOf(obj) == -1) {
    //             $scope.execute_host.push(obj);
    //             console.log($scope.execute_host);
    //         }
    //
    //     }
    // };
    //
    // $scope.execute_job = function () {
    //     if ($scope.execute_host.length) {
    //         loading.open();
    //         certificateService.execute_job_host({}, $scope.execute_host, function (res) {
    //             loading.close();
    //             if (res.result) {
    //                 msgModal.open('info', '执行成功')
    //             } else {
    //                 msgModal.open('error', res.message)
    //             }
    //         })
    //     } else {
    //         msgModal.open('error', '请选择主机')
    //     }
    //
    // };


    $scope.search_host_test = function () {
        if ($scope.host_filter.ip){

        }else {
            msgModal.open('error', '请输入IP')
        }
    }

}])
;