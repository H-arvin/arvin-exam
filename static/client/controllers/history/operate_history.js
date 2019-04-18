/**
 * Created by arvin on 2019-1-5 0005.
 */
controllers.controller("operate_history", ["$scope", "certificateService", "$modal", "loading", "confirmModal", "msgModal", "$location", function ($scope, certificateService, $modal, loading, confirmModal, msgModal, $location) {
    $scope.host_filter = {biz_id: '', time: ''};
    $scope.biz_id = 0;
    $scope.biz_list = [];
    $scope.job_log = [];
    console.log('aaaaa');
    $scope.init = function () {
        loading.open();
        certificateService.get_biz_list({}, {}, function (res) {
            $scope.biz_list = res.data;
            loading.close()
        });
        certificateService.get_job({}, {}, function (res) {
            $scope.job_log = res.data
        })
    };
    $scope.init();


    $scope.gridOption = {
        data: 'job_log',
        columnDefs: [
            {field: 'biz_name', displayName: '业务'},
            {field: 'execute_user', displayName: '用户'},
            {field: 'job_id', displayName: '作业ID'},
            {field: 'exectue_time', displayName: '操作时间'},
            {field: 'ip_list', displayName: '主机列表'},
            {field: 'job_status', displayName: '状态'},
            {field: 'ip_log', displayName: '日志'}
        ]
    };

    $scope.search =function () {
        if ($scope.host_filter.biz_id || $scope.host_filter.time){
            certificateService.filter_log({},$scope.host_filter,function (res) {
                $scope.job_log = res.data
            })
        }else {
            msgModal.open('error','请填写筛选条件')
        }
    }


}]);