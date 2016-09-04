/**
 * Created by lightless on 2016/9/4.
 */


var userHomeApp = angular.module("UserHome", ['ui.router']);

userHomeApp.controller("bodyController", function ($scope) {
    $scope.test = "123";
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
            // 'main_window': {
            //     templateUrl: "/tpl/Frontend/Home/docker.html"
            // }
        }
    });
});


