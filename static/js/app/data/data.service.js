'use strict';

angular.module('data').
    factory('Data', function($resource) {
        var url = '/api/routines/'
        return $resource(url, {}, {
            query: {
                method: "GET",
                params: {},
                isArray: true,
                cache: false,
                }
            },
            get: {
                method: "GET",
                params: {},
                isArray: false,
                cache: false,
            }
        )
      }
 )