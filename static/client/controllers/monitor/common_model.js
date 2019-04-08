/**
 * Created by arvin on 2019-1-6 0006.
 */
controllers.controller("common_model", ["$scope", "errorModal", "$interval", "sysService", function ($scope, errorModal, $interval, sysService) {

    $scope.uploadItem = function () {
        ajaxFileUpload("#uploadInfo");
    };

    var ajaxFileUpload = function (input_id) {
        $scope.file_list = [];
        var fd = new FormData();
        var files = $(input_id).get(0).files;
        fd.append("upload", files.length);
        var name_path = "test_";
        fd.append("file_path", name_path);
        for (var i = 0; i < files.length; i++) {
            if (files[i].size > 10485760) {
                errorModal.open(["文件大小不能超过10M！"]);
                $scope.file_list = [];
                return;
            }
            var file_name = files[i].name.toLowerCase();
            // if (files[i].name.split(".")[1] != 'txt') {
            //     errorModal.open(["只能上传.txt文件"]);
            //     $scope.file_list = [];
            //     return;
            // }
            fd.append("upfile" + i, files[i]);

            $scope.file_list.push({
                name: files[i].name,
                size: ((files[i].size / 1024) + "").split(".")[0] + "KB",
                process: 1
            })
        }
        console.log(fd.upfile);
        for (var i = 0; i < $scope.file_list.length; i++) {
            $interval(changeProcess, 2000, 50, true, $scope.file_list[i])
        }
        $.ajax({
            url: site_url + "upload_info/",
            type: "POST",
            processData: false,
            contentType: false,
            data: fd,
            success: function (res) {
                if (res.result) {
                    $scope.setComplete();
                }
                else {
                    $scope.removeComplete();
                    errorModal.open(res.data);

                }
            }
        });
    };

    $scope.fileGrid = {
        data: "file_list",
        columnDefs: [
            {field: "name", displayName: "文件名"},
            {field: "size", displayName: "文件大小", width: 100},
            {
                displayName: "进度", width: 160,
                cellTemplate: '<div style="width:100%;padding:5px 10px;text-align: center">\
                <div class="progress progress-striped active" style="height:25px;margin-top: 0">\
                    <div class="progress-bar progress-bar-success" style="width: {{row.entity.process}}%;padding-top:2px;">{{row.entity.process}}%</div>\
                </div>\
                </div>'
            }
        ]
    };

    var changeProcess = function (one_file) {
        if (one_file.process >= 90) {
            return;
        }
        var a = Math.floor(Math.random() * 10 + 1);
        one_file.process += a;
    };

    $scope.setComplete = function () {
        for (var i = 0; i < $scope.file_list.length; i++) {
            $scope.file_list[i].process = 100;
        }
    };

    $scope.removeComplete = function () {
        $scope.file_list = [];
    };

    $scope.site_url = window.location.href.split("#")[0];
    $scope.uploadOption = {
        //select：按钮标题
        select: "点击上传logo",
        //saveUrl：上传地址
        saveUrl: $scope.site_url + "arvin_test?app_id=1",
        //success：上传成功的回调函数
        success: function (e) {
            if (!e.response.result) {
                msgModalN(e.response.message);
            }
            //刷新log
            console.log(e.response)
        },
        max_size: 100 //允许上传的图片大小
    }

}]);