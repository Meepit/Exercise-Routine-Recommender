'use strict'

angular.module('recommend').component('recommend', {
    templateUrl: '/api/templates/recommendview.html',
    controller: function($cookies, $http, $location, $routeParams, $rootScope, $scope){
           $scope.routineTypes = [
                [0, "Strength"],
                [1, "Hypertrophy (Mass gain)"],
           ]

           $scope.equipmentAvailability = [
                [0, "Basic equipment (Barbell, bench, squat rack)"],
                [1 , "Extensive equipment (full gym)"],
            ]

            $scope.priorityField = [
                ["routine_type", "Routine Type"],
                ["equipment_needed", "Equipment Availability"],
                ["days_per_week", "Days Per Week"],
                ["session_length", "Session Length"],
            ]

           $scope.daysPerWeek = [3,4,5]
           $scope.sessionLength = 60

           $scope.routineData = {
                "routineType": "",
                "equipmentNeeded": "",
                "daysPerWeek": "",
                "sessionLength": "",
                "priorityField": "",
           }

           $scope.postRoutine = function(){
                $scope.gotRoutine = true;
                $http.post('/api/recommend/', {
                    "routine_type": $scope.routineData.routineType[0],
                    "equipment_needed": $scope.routineData.equipmentNeeded[0],
                    "days_per_week": $scope.routineData.daysPerWeek,
                    "session_length": $scope.routineData.sessionLength * 1,
                    "priority_field": $scope.routineData.priorityField[0]
                }).then(function(response){
                    $scope.chosenRoutine = response.data.Routine_Name
                    $scope.chosenRoutineID = response.data.Routine_ID[0]
                    // TODO: Save routine in cookies if not logged in and user wants to register
                }, function(response){
                    console.log(response)
                })
           }

           $scope.saveRoutine = function(){
                if($cookies.get("token")){
                    //logged in.
                    var token = $cookies.get("token")
                    $http.put('/api/users/' + $cookies.get("username") + "/", {
                        "routine_id": $scope.chosenRoutineID
                    }, {headers: {"Authorization": "JWT " + token}}).then(function(response){
                        console.log("Set routine")
                    })
                } else {
                    // Save routine in cookie to be added if user registers
                    $cookies.put("savedRoutine", $scope.chosenRoutineID)
                    console.log("Cookie created")
                }
           }

    }
})