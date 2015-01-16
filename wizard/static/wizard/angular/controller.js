var SVOapp = angular.module('SVOapp', ['ui.bootstrap']);

SVOapp.controller('SVOcontroller', function ($scope, $http) {
	
	$scope.accordion_status = {
		first_opened: true,
		user_selections_opened: false
	};
	
	$http.get('http://benjmam-pc.oma.be:8000/api/v1/dataset', {params: {limit: 0}}).success(function(data)
	{
		$scope.datasets = data.objects;
		// Hide all datasets at first
		$scope.datasets.forEach(function(dataset){dataset.is_hidden = true; $scope.accordion_status[dataset.id] = false;});
	});
	
	$http.get('http://benjmam-pc.oma.be:8000/api/v1/user_data_selection/?format=json&user=bmampaey').success(function(data)
	{
		$scope.user_data_selections = data.objects;
	});
	
	
	window.my_scope = $scope;
});
