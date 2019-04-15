/**
 * Created by arvin on 2019-1-6 0006.
 */
controllers.controller("chart_demo", ["$scope", function ($scope) {
    /*柱状图使用样例*/
    $scope.test_column = [
        {name: 'Windows服务器', data: [1]},
        {name: 'AD服务器', data: [2], color: "#4cb5b0"},
        {name: 'TEST服务器', data: [2]}
    ];
    $scope.test_chart = {
        //柱状图标题
        title: {text: '服务器', enabled: false},
        //y轴
        yAxis: {
            title: {text: '数目'}, //y轴标题
            lineWidth: 2, //基线宽度1
            //tickPositions: [0, 1, 2, 3, 4]
        },
        //提示框位置和显示内容
        tooltip: {
            headerFormat: '<table\>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f} 台</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true,
            positioner: function () {
                return {x: 80, y: 80}
            }
        },
        data: "test_column"
    };

    $scope.serverRepairList = [{y: 2, name: "已修复"}, {y: 7, name: "未修复"}];
    $scope.updateInfoReports = {
        data: "serverRepairList",
        title: {text: '服务器修复状况报表', enabled: true},
        unit: "台",
        size: "200px"
    };

        /*折线图
    * highcharts配置文档：https://www.helloweba.com/view-blog-156.html
    * */
    $scope.taskReports = {
        data: "taskList",
        chart: {type: 'line'},//数据列类型，支持 area, areaspline, bar, column, line, pie, scatter or spline
        title: {text: '每月历史巡检次数统计', enabled: true},
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
    //纵坐标
    $scope.taskList = [{'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 58, 32, 5], 'name': '本月巡检次数'}];
    //横坐标,不填为默认值
    $scope.taskReports.xAxis.categories = ['9月', '10月', '11月', '12月', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月'];

}]);