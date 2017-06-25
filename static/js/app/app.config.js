'use strict';

angular.module('routine').
    config(
        function(
            $locationProvider,
            $resourceProvider,
            $routeProvider
            ){

            $locationProvider.html5Mode({
                enabled:true
                })
            $resourceProvider.defaults.stripTrailingSlashes = false;
            $routeProvider.
                when("/", {
                    template: "Home"// Create home template
                }).
                when("/login", {
                    template: "Login page"// create login template
                }).
                when("/routines", {
                    template: "<routine-list></routine-list>"
                }).
                when("/routines/:id", {
                    template: "<routine-detail></routine-detail>"
                }).
                otherwise({
                    template: "Page not found"
                })
         });