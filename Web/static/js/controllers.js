/**
 * Created by lightless on 2016/9/6.
 */

userHomeApp.controller("bodyController", function ($scope) {
    $scope.test = "123";
});

// 侧边栏高亮显示的控制器
userHomeApp.controller("SidebarController", function ($scope, $log, $location) {
    $scope.activeSidebar = $location.$$path.split("/")[1];
});

userHomeApp.controller("createNewDocker", function ($scope, $http, $log, $window) {

    // API版本，后续更新时，保持接口一致，只需更改这个就可以了
    var API_VERSION = "v1";

    // 系统镜像版本信息
    $scope.versions = [{"version": "None"}];
    $scope.ver_id = null;
    $scope.port = null;
    $scope.createDockerBtn = false;

    // 获取生成表单用的信息
    $http({
        method: 'GET',
        url: "/api/" + API_VERSION + "/get_info"
    }).success(function (response) {
        if (response.code != 1001) {
            $scope.errorMessage = response.message;
            return false;
        } else {
            $scope.info = response.info;
        }
    }).error(function () {
        $log.error("拉取操作系统版本信息失败！");
        $scope.errorMessage = "Error when getting op system...";
        return false;
    });

    // 选择系统镜像
    $scope.funcSystemImage = function (imageName) {
        $scope.imageName = imageName;
        $scope.versions = $scope.info[imageName];
        // $log.debug($scope.versions);
    };

    // 选择镜像版本
    $scope.funcImageVersion = function (ver_id) {
        $scope.ver_id = ver_id;
    };

    // 创建镜像
    $scope.funcCreateDocker = function () {

        // 禁用按钮
        $scope.createDockerBtn = true;

        // 整理数据
        var payload = {
            "version_id": $scope.ver_id,
            "port": $scope.port,
        };
        var csrfToken = $window.document.getElementsByName("csrf-token")[0].content;
        $http({
            method: "POST",
            url: "/api/" + API_VERSION + "/create_docker",
            data: payload,
            headers: {"X-CSRFToken": csrfToken}
        }).success(function (data) {
            if (data.code != 1001) {
                $scope.errorMessage = data.message;
            } else {
                $scope.alertTag = 'success';
                $scope.errorMessage = data.message;
            }
        }).error(function () {
            $scope.errorMessage = "Create a docker failed.";
            return false;
        });

    }
});
