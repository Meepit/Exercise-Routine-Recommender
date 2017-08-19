'use strict';

angular.module('routineList').component('routineList', {
    templateUrl: '/api/templates/routines.html',
    controller: function(RoutineData, WorkoutData, $scope, $cookies, $http){
        $scope.loggedIn = $cookies.get("token")
        $scope.routines = RoutineData.get()

        $scope.changeRoutine = function(routineID){
            $http({
              method: "PUT",
              url: '/api/users/' + $cookies.get("username") + '/',
              data: {'routine_id': routineID},
              headers: {'Authorization': 'JWT ' + $cookies.get("token")}
            }).then(function(response){
                $scope.success = true;
            })
        }
    }
  }
)