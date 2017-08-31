angular.module('navBar').component('navBar', {
    templateUrl: '/api/templates/navbar.html',
    controller: function($scope, $cookies, $http, $location) {
        // Everything bound to $scope.watch is checked for changes during angular's digest cycle

        $scope.loggedIn = false
        $scope.$watch(function() {
            if ($cookies.get("token")) {
                $scope.loggedIn = true
            } else {
                $scope.loggedIn = false
            }
        })

        // Called when certain pages are clicked in the nav bar which may redirect user to login page if token expired.
        $scope.checkToken = function(redirect) {
            $http({
                url: '/api/poll/',
                method: 'GET',
                headers: {
                    'Authorization': 'JWT ' + $cookies.get("token")
                }
            }).then(function(response) {
            }, function(response) {
                if (response.status == 401) {
                    console.log("Unauthenticated")
                    $cookies.remove("token")
                    if (redirect) {
                        $location.path('/login')
                    }
                }
            })
        }
    }
})