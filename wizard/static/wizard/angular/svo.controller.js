var app = angular.module('SVOapp');

app.controller('SVOCtrl', function ($scope, $http) {
	
	$scope.accordion_status = {
		first_opened: true,
		user_data_selection_opened: false
	};
	
	$scope.datasets = [];
	
	$scope.open_dataset = function(dataset) {
		dataset.is_hidden = false;
		$scope.accordion_status[dataset.id] = true;
		if($scope.datasets.indexOf(dataset) < 0)
		{
			$scope.datasets.push(dataset);
		}
	};
	
	console.log("SVOCtrl scope", $scope);
});
