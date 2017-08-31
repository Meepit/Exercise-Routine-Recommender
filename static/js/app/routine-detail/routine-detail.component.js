'use strict';

angular.module('routineDetail').component('routineDetail', {
    templateUrl: 'api/templates/routinedetail.html',
    controller: function(RoutineData, $scope, $location, $rootScope, $routeParams) {
        $scope.routine = RoutineData.query({
            "id": $routeParams.id
        })
    }
})