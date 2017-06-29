'use strict';
// Define factory to return resource
angular.module('data').
    factory('RoutineData', function($resource) {
        return $resource('/api/routines/:id/', {}, {
            get: { // Get entire routine list
                method: "GET",
                params: {"id": "@id"},
                isArray: true,
                },
             query: { // filter by id
                method: "GET",
                params: {"id": "@id"}
                },
                });
});

angular.module('data').
    factory('WorkoutData', function($resource) {
        return $resource('/api/workouts/:id/', {}, {
            get: {
                method: "GET",
                params: {"id": "@id"},
                isArray: true,
                },
             query: { // filter by id
                method: "GET",
                params: {"id": "@id"}
                },
                });
});

// Have the factory take a function as a parameter so that we can pass token to it
// Allowing authentication of request
angular.module('data').
    factory('UserData', ['$resource', function($resource){
        return {
            userData: function(token){
                return $resource('/api/users/:username/progress/', {}, {
                    get: {
                        method: "GET",
                        params: {"username": "@username"},
                        isArray: true,
                        headers: {
                            'Authorization': 'JWT ' +  token
                        }
                    }
                })
            }
        }
    }])


//    factory("Data", function($resource) {
//        var url = '/api/routines/'
//        return $resource(url, {}, {
//            query: {
//               method: "GET",
//                params: {},
//                isArray: true,
//                cache: false,
//                transformResponse: function(data, headersGetter, status){
//                    console.log(data)
//                    var finalData = angular.fromJson(data)
//                    return finalData.results
//                }
//            },
//            get: {
//                method: "GET",
//                params: {"id": "@id"},
//                isArray: true,
//                cache: false,
//            }
//        }
//    )
//});