'use strict';

angular.module('accountView').component('accountView', {
    templateUrl: 'api/templates/accountview.html',
    controller: function($cookies, $scope, $location, $http, RoutineData) {
        // Update password
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

        // On page load, check if user is authenticated.
        // If user is authenticated, display profile information.
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