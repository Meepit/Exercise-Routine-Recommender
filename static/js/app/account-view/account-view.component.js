'use strict';

angular.module('accountView').component('accountView',{
    templateUrl: 'api/templates/accountview.html',
    controller: function($cookies, $scope, $location, $http, $routeParams){
            var loggedIn = $cookies.get("token")
            if(loggedIn == null){
                $scope.errors = "Please login to view this page"
            }
            else {
                $scope.username = $cookies.get("username")
                $http({
                    method: 'GET',
                    url: '/api/users/' + $scope.username + '/',
                    headers: {"Authorization": "JWT " + $cookies.get("token")}
                }).then(function(response){
                    console.log(response)
                }, function(response){
                    console.log(response)
                })
            }
        }
    })