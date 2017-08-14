'use strict'

angular.module('registrationView').component('registrationView', {
    templateUrl: '/api/templates/registration.html',
    controller: function($scope){
        $scope.userData = {
            firstName: "",
            username: "",
            password: "",
            passwordVerify: "",
            email: "",
        }

      $scope.charRestrict = {
        regExp: /[{}\[\]|\\/'()";:<>]+/i,
        test: function(val) {
             return !this.regExp.test(val);
      }
    };

        $scope.registerUser = function(){

        }

    }
})