'use strict';

angular.module('progressView').component('progressView', {
        templateUrl: 'api/templates/progress.html',
        controller: 'progressController', // Only seems to function under a named controller
})
.controller("progressController", function ($scope, $cookies, $http, UserData) {

            var loggedIn = $cookies.get("token")
            if (loggedIn == null){
                $scope.errors = "Please login to view this page"
            }
            else{
                // user logged in
                var username = $cookies.get("username")
                var token = $cookies.get("token")

                $scope.data = [[]] // Data the graph will be generated from
                $scope.labels = [] // x axis label ticks for graph

                $scope.exercises = []
                $scope.allExercises = []

                $http({
                    method: 'GET',
                    url: '/api/exercises/',
                }).success(function(data){
                    for(var i=0; i<data.length; i++){
                        $scope.allExercises.push([data[i].id, data[i].name])
                    }
                })

                // Add lists to $scope.exercises in form of [E1, E2]
                // Where E1 is an integer id for the exercise, E2 is a string for the exercise name
                $http({
                    method: 'GET',
                    url: '/api/progress/',
                    headers: {
                        'Authorization': "JWT " + token
                        }
                    }).success(function(data){
                    // Add exercise name to array only if it has not already been added
                        var exercise_names = {}
                        for(var i=0; i<data.length; i++){
                            if (!(data[i].exercise_name in exercise_names)){
                            exercise_names[data[i].exercise_name] = 0
                            $scope.exercises.push([data[i].exercise_id, data[i].exercise_name])
                            }
                        }
                    })

                $scope.selectedExercise = [1, "benchpress 5x5"];

                $scope.progressList = []


                var genGraph = function(){
                    // Reset graph data
                    $scope.data = [[]]
                    $scope.labels = []
                    $scope.series = [$scope.selectedExercise[1]];
                    // Sort data by date
                    $scope.exerciseData = UserData.userData(token).get({"username": username}, function(data){
                        data.sort(function(a,b){
                                if(a.date < b.date) return -1;
                                if(a.date > b.date) return 1;
                                return 0;
                        })
                        for(var i=0; i < data.length; i++){
                            $scope.progressList.push([data[i].id,
                                                   data[i].date + " " + data[i].exercise_name + " " + data[i].quantity])
                            if(data[i].exercise_id == $scope.selectedExercise[0]){
                                $scope.data[0].push(data[i].quantity)
                                $scope.labels.push(data[i].date)
                            }
                        }
                    })
                }

                $scope.$watch('selectedExercise', genGraph)

                $scope.postProgress = function(){
                    $scope.postSuccMsg = ""
                    $scope.postErrMsg = ""
                    $http.post('/api/progress/', {
                        "date": $scope.postDate.toJSON().slice(0,10),
                        "quantity": $scope.postQuantity,
                        "exercise": "http://localhost:8000/api/exercises/" + $scope.postExercise[0] +"/",
                        "user": "http://localhost:8000/api/users/1/"
                        }, {headers:{"Authorization": "JWT " +token}}).then(function(response){
                            $scope.postSuccMsg = response.statusText
                            genGraph()
                        }, function(response){
                            $scope.postErrMsg = response.statusText})
                }

               $scope.deleteProgress = function(){
                    if($scope.selectedProgress){
                        for(var i=0; i<$scope.selectedProgress.length; i++){
                            $http({
                                method: 'DELETE',
                                url: '/api/progress/' + $scope.selectedProgress[i][0] + '/',
                                headers: {
                                    "Authorization": "JWT " + token
                                }
                            }).then(function(response){
                                // Display success msg
                                $scope.deleteSuccMsg = response.statusText
                                genGraph()
                            }, function(response){
                                // Display something went wrong
                                $scope.deleteErrMsg = response.statusText
                            })
                        }
                    } else {
                        // Show error msg
                    }
               }

              $scope.series = [$scope.selectedExercise[1]];
              // $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
              $scope.options = {
                scales: {
                  yAxes: [
                    {
                      id: 'y-axis-1',
                      type: 'linear',
                      display: true,
                      position: 'left'
                    },

                  ]
                }
               };
           }
});