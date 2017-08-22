'use strict';

angular.module('homeView').component('homeView', {
    templateUrl: '/api/templates/home.html',
    controller: function($scope, $location){
	$scope.goToClassification = function(){
	    $location.path('/recommend')
	}
    }
})
