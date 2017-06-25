'use strict';

angular.module('navBar').
    directive('navBar', function($cookies, $location){
        return {
            //restrict: "E",
            templateUrl: "api/templates/navbar.html",
        }
    }
)