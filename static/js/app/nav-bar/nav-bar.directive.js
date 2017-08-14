'use strict';

angular.module('navBar').
    directive('navBar', function($cookies, $location){
        return {
            restrict: "E",
            templateUrl: "/api/templates/navbar.html",
            link: function(scope, element, attr){
                // loggedIn tracks whether loggedIn cookie is available or not
                // if available, login button becomes logout in navbar html
                scope.loggedIn = false
                scope.$watch(function(){
                    if ($cookies.get("token")){
                        scope.loggedIn = true
                    }
                    else {
                        scope.loggedIn = false
                    }
                })
            }
        }
    }
)
