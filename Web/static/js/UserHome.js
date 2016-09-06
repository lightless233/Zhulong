/**
 * Created by lightless on 2016/9/4.
 */


var userHomeApp = angular.module("UserHome", ['ui.router']);

userHomeApp.controller("bodyController", function ($scope) {
    $scope.test = "123";
});

userHomeApp.controller("addDockerController", function ($scope, $http, $log) {

    // API的版本
    var API_VERSION = "v1";

    // 选择操作系统的buttons
    $scope.activeButtonClass = false;
    $http({
        method: 'GET',
        url: "/api/" + API_VERSION + "/get_op_systems"
    }).success(function (data) {
        if (data.code != 1001) {
            $scope.errorMessage = data.messag;
        } else {
            $scope.OPSystemButtons = data.ops;
        }
    });
    // $scope.OPSystemButtons = ["ubuntu", "centos", "debian"];

    // 操作系统的版本列表
    $scope.op_versions = {};
    $scope.selectedOPVersion = "";

    $scope.clickOPSystemButton = function (op) {
        $scope.activeButtonClass = op;
        $log.debug(op);

        // 从后台获取操作系统版本信息
        $http({
            method: 'GET',
            url: "/api/" + API_VERSION + "/get_op_system_versions?op=" + op
        }).success(function (data, header, config, status) {
            $log.debug(data);
            if (data.code != 1001) {
                $scope.errorMessage = data.message;
            } else {
                $scope.op_versions = data.versions;
            }
        }).error(function (data, header, config, status) {
            $log.error("拉取操作系统版本信息失败！");
            $scope.errorMessage = "Error when getting op system..."
        });
    }
});


// 路由
userHomeApp.config(function ($stateProvider, $urlRouterProvider) {
    // 默认路由
    $urlRouterProvider.otherwise("/");

    // 路由配置
    $stateProvider.state("index", {
        url: "/",
        views: {
            '': {
                templateUrl: "/tpl/Frontend/Home/home_base.html"
            },
            'sidebar': {
                templateUrl: "/tpl/Frontend/Home/sidebar.html"
            },
            // 'main_window': {
            //     templateUrl: "/tpl/Frontend/Home/docker.html"
            // }
        }
    });

    $stateProvider.state('docker', {
        url: "/docker",
        views: {
            '': {
                templateUrl: "/tpl/Frontend/Home/home_base.html"
            },
            'sidebar': {
                templateUrl: "/tpl/Frontend/Home/sidebar.html"
            },
            'main_window': {
                templateUrl: "/tpl/Frontend/Home/docker.html"
            }
        }
    });

    $stateProvider.state('addDocker', {
        url: "/docker/add",
        views: {
            "": {
                templateUrl: "/tpl/Frontend/Home/home_base.html"
            },
            'sidebar': {
                templateUrl: "/tpl/Frontend/Home/sidebar.html"
            },
            'main_window': {
                templateUrl: "/tpl/Frontend/Home/docker_add.html"
            }
        }
    });
});

