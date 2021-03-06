controllers.controller("site", ["$scope", function ($scope) {
    $scope.menuList = [
        {
            displayName: "主机管理", iconClass: "fa fa-lg fa-home", url: "#/monitor_host"
        },
        {
            displayName: "test页面", iconClass: "fa fa-lg fa-gear", children: [
                // {displayName: "monitor detail", url: "#/monitor_detail"},
                {displayName: "common model", url: "#/common_model"},
                {displayName: "chart model", url: "#/chart_demo"}
            ]
        }
    ];

    $scope.menuOption = {
        data: 'menuList',
        locationPlaceHolder: '#locationPlaceHolder',
        adaptBodyHeight: CWApp.HeaderHeight + CWApp.FooterHeight
    };

}]);