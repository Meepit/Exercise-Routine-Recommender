'use strict';

angular.module('passwordCheck').
    directive('passwordCheck', function(){
        return {
            require: "ngModel",
            scope: {
                otherModelValue: "=passwordCheck"
            },
            link: function(scope, element, attributes, ngModel){
                ngModel.$validators.passwordCheck = function(modelValue) {
                    return modelValue == scope.otherModelValue;
                };

                scope.$watch("otherModelValue", function() {
                    ngModel.$validate();
                });
            }
        };
    });