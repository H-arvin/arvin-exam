controllers.controller("site", ["$scope", function ($scope) {
    $scope.menuList = [
        {
            displayName: "主机管理", iconClass: "fa fa-lg fa-home", url: "#/monitor_host"
        }
    ];

    $scope.menuOption = {
        data: 'menuList',
        locationPlaceHolder: '#locationPlaceHolder',
        adaptBodyHeight: CWApp.HeaderHeight + CWApp.FooterHeight
    };

}]);