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
                    template: "Home page"// Create home template
                }).
                when("/login", {
                    template: "Login page"// create login template
                }).
                otherwise({
                    template: "Page not found"
                })
         });