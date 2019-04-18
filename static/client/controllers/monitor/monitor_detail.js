/**
 * Created by arvin on 2019-1-5 0005.
 */
controllers.controller("monitor_detail", ["$scope", "monitorService", "$location", "loading", "msgModal", function ($scope, monitorService, $location, loading, msgModal) {
    $scope.return_page = $location.search().return_page;
    var host_obj = $location.search().host_obj;
    var ip_address = $location.search().ip_address;

    // 饼图
    $scope.serverRepairList = [{y: 1, name: "已用内存"}, {y: 1, name: "剩余内存"}];
    $scope.updateInfoReports = {
        data: "serverRepairList",
        title: {text: '服务器内存使用表', enabled: true},
        unit: "",
        size: "200px"
    };

    /*折线图
     * highcharts配置文档：https://www.helloweba.com/view-blog-156.html
     * */
    $scope.taskReports = {
        data: "taskList",
        chart: {type: 'line'},//数据列类型，支持 area, areaspline, bar, column, line, pie, scatter or spline
        title: {text: '服务器负载统计', enabled: true},
        xAxis: {
            categories: []
        },
        //提示框位置和显示内容
        tooltip: {
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f}</b></td></tr>',
            headerFormat: ""
        }
    };
    // //纵坐标
    // $scope.taskList = [{'data': [1,2,3,4,5,6,7], 'name': '最近一小时服务器负载数'}];
    // //横坐标,不填为默认值
    // $scope.taskReports.xAxis.categories = ['10:01','10:02','10:03','10:04','10:05','10:06','10:07'];

    $scope.disk_info = [];
    $scope.gridOption = {
        data: 'disk_info',
        columnDefs: [
            {field: 'file_sys', displayName: '文件系统'},
            {field: 'capacity', displayName: '总大小'},
            {field: 'used', displayName: '已用大小'},
            {field: 'un_use', displayName: '可用大小'},
            {field: 'usage_rate', displayName: '使用率'},
            {field: 'mount_on', displayName: '挂载点'}
        ]
    };

    $scope.init = function (ip_address) {
        loading.open();
        console.log(host_obj);
        console.log(host_obj);
        monitorService.get_monitor_detail({}, {"ip_address":ip_address}, function (res) {
            loading.close();
            if (res.result) {
                var mem = res.mem;
                $scope.serverRepairList[1].y = mem.unuse;
                $scope.serverRepairList[0].y = mem.used;
                $scope.disk_info = res.disk_info;
                var load_avg = res.load_avg;
                console.log(load_avg);
                // $scope.taskReports.xAxis.categories = load_avg.x;
                //  $scope.taskList[0].data = load_avg.y;
                //纵坐标
                $scope.taskList = [{'data': load_avg.y, 'name': '最近一小时服务器负载数'}];
                //横坐标,不填为默认值
                $scope.taskReports.xAxis.categories = load_avg.x;
                console.log($scope.taskReports.xAxis.categories);
                console.log($scope.taskList[0].data);
            } else {
                msgModal.open("error", "查询性能数据失败")
            }

        })
    };
    $scope.init(ip_address);

}]);
