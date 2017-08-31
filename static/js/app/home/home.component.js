'use strict';

angular.module('homeView').component('homeView', {
    templateUrl: '/api/templates/home.html',
    controller: function($scope, $location, RoutineData, $http, $cookies) {

        $scope.goToClassification = function() {
            $location.path('/recommend')
        }

        // Format routine data as hash of arrays for each day, allowing for easier display in html.
        var genRoutineSchedule = function() {
            var routine = RoutineData.query({
                "id": $scope.routineID
            }, function(success) {
                var increment = Math.round(7 / routine.days_per_week);
                var daysOfWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
                var exampleWeek = {
                    "Mon": [" ", ["Rest"]],
                    "Tue": [" ", ["Rest"]],
                    "Wed": [" ", ["Rest"]],
                    "Thu": [" ", ["Rest"]],
                    "Fri": [" ", ["Rest"]],
                    "Sat": [" ", ["Rest"]],
                    "Sun": [" ", ["Rest"]]
                };
                var pointer = 0
                var counter = 0
                for (var i = 0; i < 7; i += increment) {
                    if (routine.days_per_week == counter) {
                        break
                    }
                    var day = daysOfWeek[i];
                    var exercises = [];
                    for (var j = 0; j < routine.workout[pointer].exercises.length; j++) {
                        exercises.push(routine.workout[pointer].exercises[j].name)
                    }
                    exampleWeek[day] = [routine.workout[pointer].name, exercises];
                    if (pointer + 1 >= routine.workout.length) {
                        pointer = 0
                    } else {
                        pointer++
                    }
                    counter++
                }
                $scope.daysOfWeek = daysOfWeek;
                $scope.exampleWeek = exampleWeek;
            });
        }

        // Only attempt to display routine table if user is logged in.
        var loggedIn = $cookies.get("token")
        if (loggedIn == null) {
            $scope.hideRoutine = true;
        } else {
            $scope.username = $cookies.get("username")
            $http({
                method: 'GET',
                url: '/api/users/' + $scope.username + '/',
                headers: {
                    "Authorization": "JWT " + $cookies.get("token")
                }
            }).then(function(response) {
                $scope.routineID = response.data.routine.id
                genRoutineSchedule()
            }, function(response) {
                console.log(response)
            })

        }


    }
})