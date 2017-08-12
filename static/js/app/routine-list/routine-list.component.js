'use strict';

angular.module('routineList').component('routineList', {
    templateUrl: '/api/templates/routines.html',
    controller: function(RoutineData, WorkoutData, $scope){
        $scope.routines = RoutineData.get()
    }
  }
)