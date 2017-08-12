'use strict'

angular.module('registrationView').component('registrationView', {
    templateUrl: '/api/templates/registration.html',
    controller: function($scope){
        $scope.userData = {
            firstName: "",
            username: "",
            password: "",
            passwordCheck: "",
            email: "",
        }

      //  $scope.errors =
      //  var clientsideValidation = function(){

 //       }

        $scope.registerUser = function(){
            // clientside validation maybe do this with $scope.$watch on userData keys
        }

    }
})