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
                    template: "<home-view></home-view>"// Create home template
                }).
                when("/login", {
                    template: "<login></login>"// create login template
                }).
                when("/routines", {
                    template: "<routine-list></routine-list>"
                }).
                when("/routines/:id", {
                    template: "<routine-detail></routine-detail>"
                }).
                when("/progress",{
                    template: "<progress-view></progress-view>"
                }).
                when("/recommend",{
                    template: "<recommend><recommend>"
                }).
                when("/my-account",{
                    template: "<account-view><account-view>"
                }).
                when("/register",{
                    template: "<registration-view><registration-view>"
                }).
                otherwise({
                    template: "<p>Page not found</p>"
                })
         });
