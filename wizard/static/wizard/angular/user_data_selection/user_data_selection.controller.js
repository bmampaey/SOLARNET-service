var user_data_selection = angular.module('user_data_selection');

user_data_selection.controller('user_data_selectionCtrl', function($scope, UserSelection) {
	
	$scope.user_data_selections = [];
	
	// Load user_data_selection
	UserSelection.get({},
		function(data) {
			console.log("Received user_data_selection: ", data);
			$scope.user_data_selections = data.objects.map(function(uds){uds.datasets = uds.data_selections.map(function(ds){return ds.dataset}); return uds});
		});
	
	console.log("user_data_selectionCtrl scope", $scope);
});
