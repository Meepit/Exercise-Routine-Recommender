'use strict'

angular.module('registrationView').component('registrationView', {
    templateUrl: '/api/templates/registration.html',
    controller: function($scope, $http, $cookies){
        $scope.userData = {
            firstName: "",
            username: "",
            password: "",
            passwordVerify: "",
            email: "",
        }

        $scope.charRestrict = {
            regExp: /[{}\[\]|\\/'()";,:<> ]+/i,
            test: function(val) {
             return !this.regExp.test(val);
        }
    };

        $scope.registerUser = function(){
            $http.post('/api/users/', {
                "first_name": $scope.userData.firstName,
                "username": $scope.userData.username,
                "password": $scope.userData.password,
                "email": $scope.userData.email
            }).then(function(response){
                  // Get JWT token and save in cookie.
                  // Check cookies for routine, if found set routine.

                  var request = {
                  method: 'POST',
                  url: 'api/auth/token/',
                  data: {
                      username: $scope.userData.username,
                      password: $scope.userData.password
                  },
                  headers: {}
                  }
                  var makeRequest = $http(request)
                  makeRequest.success(function(data, status, headers, config){
                      $cookies.put("token", data.token)
                      $cookies.put("username", $scope.userData.username)
                      console.log($scope.userData.username)
                  })
                  makeRequest.error(function(data, status, headers, config){
                       console.log("Error ", data)
                  })


                  if($cookies.get("savedRoutine")) {
                      // Set routine to saved routine
                      var token = $cookies.get("token")
                      console.log("Saved token: " + token)
                      $http.put('/api/users/' + $scope.userData.username + "/", {
                          "routine_id": $cookies.get("savedRoutine")
                      }, {headers: {"Authorization": "JWT " + token}}).then(function(response){
                          console.log("Set routine")
                      })
                  } else {
                      console.log("No saved routine")
                  }

                console.log(response)
            }, function(response){
                // Handle errors here like account name taken
                var data = response.data
                $scope.registerErrors = []
                for(var i=0; i<Object.keys(data).length; i++){
                    var key = Object.keys(data)[i]
                        $scope.registerErrors.push(key + ": " + data[key][0])
                }
            })
            }
        }
    })
