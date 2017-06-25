'use strict';

angular.module('routineList').component('routineList', {
    templateUrl: '/api/templates/routines.html',
    controller: function(RoutineData, WorkoutData, $cookies, $location, $routeParams, $rootScope, $scope, $http){
        $scope.routines = RoutineData.get()
    }
  }
)