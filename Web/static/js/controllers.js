/**
 * Created by lightless on 2016/9/6.
 */

userHomeApp.controller("bodyController", function ($scope) {
    $scope.test = "123";
});

userHomeApp.controller("SidebarController", function ($scope, $log, $location) {
    $scope.activeSidebar = null;
    $scope.activeSidebar = $location.$$path.split("/")[1];
    $log.debug("sidebar controller click.")
});

userHomeApp.controller("addDockerController", function ($scope, $http, $log, $window) {
    // todo: 拆分这个controller
    // API的版本
    var API_VERSION = "v1";

    // 选择操作系统的buttons
    $scope.activeButtonClass = false;
    $http({
        method: 'GET',
        url: "/api/" + API_VERSION + "/get_op_systems"
    }).success(function (data) {
        if (data.code != 1001) {
            // 状态码失败
            $scope.errorMessage = data.messag;
        } else {
            // 正常
            $scope.OPSystemButtons = data.ops;
        }
    }).error(function (data) {
        $log.error("拉取系统镜像信息失败");
        $scope.errorMessage = "Error while pulling operation system...";
        return false;
    });

    // 操作系统的版本列表
    $scope.op_versions = {};
    $scope.selectedOPVersion = "";

    // base components
    $scope.selectedBaseCom = {};
    $scope.baseComVersions = {};
    // 用户选择的基础组件版本信息
    $scope.userSelectComVersions = {};

    $scope.alertTag = 'danger';
    $scope.addDockerBtn = false;

    // 获取基础组件的信息
    // todo: 与上面的API合并，减少请求次数
    $http({
        method: "GET",
        url: "/api/" + API_VERSION + "/get_base_components"
    }).success(function (data) {
        if (data.code != 1001) {
            $scope.errorMessage = "Error while pull base components information...";
            return false;
        } else {
            $scope.baseComs = data.data;
            // 提取其中的versions信息
            for(var i = 0; i < data.data.length; ++i) {
                var t = data.data[i];
                for (var j = 0; j < t.data.length; ++j) {
                    $scope.baseComVersions[t.data[j].com_name] = t.data[j];
                }
            }
        }
        // $log.debug($scope.baseComVersions);
    }).error(function (data) {
        $log.error("拉取基础组件信息失败");
        $scope.errorMessage = "Error while pulling base components...";
        return false;
    });

    // 选择操作系统的按钮
    $scope.clickOPSystemButton = function (op) {
        $scope.activeButtonClass = op;
        // 从后台获取操作系统版本信息
        $http({
            method: 'GET',
            url: "/api/" + API_VERSION + "/get_op_system_versions?op=" + op
        }).success(function (data) {
            if (data.code != 1001) {
                $scope.errorMessage = data.message;
            } else {
                $scope.op_versions = data.versions;
            }
        }).error(function (data) {
            $log.error("拉取操作系统版本信息失败！");
            $scope.errorMessage = "Error when getting op system...";
            return false;
        });
    };

    // 选择基础组件的按钮
    $scope.clickBaseComBtn = function(baseCom) {
        // 如果不存在就推进去，否则就删去
        if ($scope.selectedBaseCom[baseCom]) {
            // 存在
            delete $scope.selectedBaseCom[baseCom];
        } else {
            // 不存在，和版本信息一起push进去
            $scope.selectedBaseCom[baseCom] = $scope.baseComVersions[baseCom];
        }
    };

    // 检查基础组件的按钮状态
    $scope.chkBaseComBtn = function(baseCom) {
        return $scope.selectedBaseCom[baseCom];
    };

    // 添加docker的按钮
    $scope.addDocker = function () {
        var data = {
            "OPSystem": $scope.activeButtonClass,
            "OPVersion": $scope.selectedOPVersion,
            "BaseCom": $scope.userSelectComVersions
        };
        // $scope.addDockerBtn = true;
        // get csrf token
        var csrfToken = $window.document.getElementsByName("csrf-token")[0].content;
        $http({
            method: "POST",
            url: "/api/" + API_VERSION + "/add_new_docker",
            data: data,
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
    };
});
