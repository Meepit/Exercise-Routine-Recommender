'use strict';

angular.module('accountView').component('accountView', {
    templateUrl: 'api/templates/accountview.html',
    controller: function($cookies, $scope, $location, $http, $routeParams, RoutineData) {

        var genRoutineSchedule = function() {
            var routine = RoutineData.query({
                "id": $scope.routineID
            }, function(success){
                var increment = Math.round(7 / routine.days_per_week);
                var daysOfWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
                var exampleWeek = {"Mon": [" ",["Rest"]], "Tue": [" ",["Rest"]], "Wed": [" ",["Rest"]],
                                   "Thu": [" ",["Rest"]], "Fri": [" ",["Rest"]], "Sat": [" ",["Rest"]],
                                   "Sun": [" ",["Rest"]]};
                var pointer = 0
                var counter = 0
                for(var i=0; i<7; i+=increment){
                    if(routine.days_per_week == counter){
                        break
                    }
                    var day = daysOfWeek[i];
                    var exercises = [];
                    for(var j=0; j<routine.workout[pointer].exercises.length; j++){
                        exercises.push(routine.workout[pointer].exercises[j].name)
                    }
                    exampleWeek[day] = [routine.workout[pointer].name, exercises];
                    if(pointer+1 >= routine.workout.length){
                       pointer = 0
                    } else {
                       pointer++
                    }
                    counter++
                }
                $scope.daysOfWeek = daysOfWeek;
                $scope.exampleWeek = exampleWeek;
                console.log(exampleWeek)
//                var pointer = 0
//                var index = 0
//                while (Object.keys(exampleWeek).length != routine.days_per_week) {
//                    var day = daysOfWeek[pointer];
//                    exampleWeek[day] = [routine.workout[index].name, routine.workout[index].exercises];
//                    pointer += increment
//                    if(index+1 >= routine.workout.length){
//                        index = 0
//                    } else {
//                        index++
//                    }
//                }
//                console.log(exampleWeek)
            });
//            console.log(routine.days_per_week)
//            var increment = Math.round(7 / routine.days_per_week);
//            var daysOfWeek = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"];
//            var exampleWeek = {};
//            var pointer = 0
//            while (Object.keys(exampleWeek).length != routine.days_per_week) {
//                var day = daysOfWeek[pointer];
//                exampleWeek[day] = routine.workout[Object.keys(exampleWeek).length].name
//                pointer++
//            }
//            console.log(exampleWeek)
        }

        $scope.updatePassword = function() {
            var username = $cookies.get('username');
            $http({
                method: 'PUT',
                url: '/api/users/' + username + '/' + 'changepassword' + '/',
                data: {
                    "old_password": $scope.passwordChange.oldPassword,
                    "new_password": $scope.passwordChange.newPassword
                },
                headers: {
                    'Authorization': 'JWT ' + $cookies.get('token')
                }
            }).then(function(response) {
                $scope.success = true;
            }, function(response) {
                $scope.errors = "";
                var data = response.data
                $scope.passwordChangeErrors = []
                for (var i = 0; i < Object.keys(data).length; i++) {
                    var key = Object.keys(data)[i]
                    $scope.passwordChangeErrors.push(key + ": " + data[key][0])
                }
            })
        }

        var loggedIn = $cookies.get("token")
        if (loggedIn == null) {
            $scope.errors = "Please login to view this page"
        } else {
            $scope.username = $cookies.get("username")
            $http({
                method: 'GET',
                url: '/api/users/' + $scope.username + '/',
                headers: {
                    "Authorization": "JWT " + $cookies.get("token")
                }
            }).then(function(response) {
                $scope.data = response.data.user
                $scope.firstName = response.data.user.first_name
                $scope.routineName = response.data.routine.name
                $scope.email = response.data.user.email
                $scope.routineID = response.data.routine.id
                genRoutineSchedule()
            }, function(response) {
                console.log(response)
            })
            $scope.passwordChange = {
                "oldPassword": "",
                "newPassword": "",
            }

        }
    }
})