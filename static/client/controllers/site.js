controllers.controller("site", ["$scope", function ($scope) {
    $scope.menuList = [
        {
            displayName: "首页", iconClass: "fa fa-lg fa-home", url: "#/home"
        },
        {
            displayName: "monitor", iconClass: "fa  fa-lg fa-camera ", children: [
            {displayName: "monitor host", url: "#/monitor_host"}
            // {displayName: "monitor detail", url: "#/monitor_detail"},
            // {displayName: "common model", url: "#/common_model"},
            // {displayName: "chart model", url: "#/chart_demo"}
        ]
        },
        {
            displayName: "history", iconClass: "fa  fa-lg fa-history ", url:"#/operate_history"
        }
    ];

    $scope.menuOption = {
        data: 'menuList',
        locationPlaceHolder: '#locationPlaceHolder',
        adaptBodyHeight: CWApp.HeaderHeight + CWApp.FooterHeight
    };

}]);