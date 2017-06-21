'use strict';

angular.module('navBar').
    directive('navBar', function($cookies, $location){
        return {
            restrict: "E",
            templateUrl: "api/templates/navbar.html",
            link: function(scope, element, attr) {
                scope.userLoggedIn = false
                scope.$watch = $cookies.get("token")
                if (token) {
                    scope.userLoggedIn = true
                    }
                else{
                    scope.userLoggedIn = false
                    }

            }
        }
    }
)