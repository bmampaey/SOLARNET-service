var DataSelectionApp = angular.module('DataSelectionApp');

DataSelectionApp.controller('DataSelectionController', function($scope, DataSelection) {
	
	$scope.data_selections = [];
	
	// Load user_data_selection
	DataSelection.get({},
		function(data) {
			console.log("Received data selections: ", data);
			$scope.data_selections = data.results;
		});
	
	console.log("DataSelectionController scope", $scope);
});
