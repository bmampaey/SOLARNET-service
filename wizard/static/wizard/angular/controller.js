var SVOapp = angular.module('SVOapp', ['ui.bootstrap']);

SVOapp.controller('datasets', function ($scope, $http) {
    $http.get('http://benjmam-pc.oma.be:8000/api/v1/dataset', {params: {limit: 0}}).success(function(data)          
  {
    $scope.datasets = data.objects;
  });

  $scope.orderProp = 'name';
});
