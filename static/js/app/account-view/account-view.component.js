'use strict';

angular.module('accountView').component('accountView',{
    templateUrl: 'api/templates/accountview.html',
    controller: function($cookies, $scope, $location, $rootScope, $routeParams){
            var loggedIn = $cookies.get("token")
            if(loggedIn == null){
                $scope.errors = "Please login to view this page"
            }
            else {
                //
            }
        }
    })