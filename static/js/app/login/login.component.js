'use strict'

angular.module('login').component('login', {
    templateUrl: '/api/templates/login.html',
    controller: function($cookies, $http, $location, $routeParams, $rootScope, $scope) {
        var url = 'api/auth/token/'
        $scope.user = {
        }
        var existingToken = $cookies.get("token")
        if (existingToken) {
            console.log("Existing token found")
            $scope.loggedIn = true;
            $cookies.remove("token")
            $scope.user = {
                username: $cookies.get("username")
            }
        }
        $scope.login = function(user) {
            // Create and make POST
            // If successful, add token and username to cookie
            var request = {
                method: 'POST',
                url: url,
                data: {
                    username: user.username,
                    password: user.password
                },
                headers: {}
            }
            var makeRequest = $http(request)
            makeRequest.success(function(data, status, headers, config) {
                $cookies.put("token", data.token)
                $cookies.put("username", user.username)
                $location.path("/")
            })
            makeRequest.error(function(data, status, headers, config) {
                $scope.loginError = data.non_field_errors.join("<br>")
                console.log("Error ", data)
            })
        }
    }
})