var datasetApp = angular.module('datasetApp', ['ngResource', 'multi-select']);

datasetApp.factory('Dataset', ['$resource',
	function($resource) {
		return $resource('/api/v1/dataset');
	}
]);

datasetApp.factory('Telescope', ['$resource',
	function($resource) {
		return $resource('/api/v1/telescope');
	}
]);

datasetApp.factory('Characteristic', ['$resource',
	function($resource) {
		return $resource('/api/v1/characteristic');
	}
]);

datasetApp.controller('datasetController', function($scope, $timeout, $filter, Dataset, Telescope, Characteristic) {
	
	// debugging hack 
	window.MY_SCOPE = $scope;
	// load instruments and characteristics
	$scope.instruments = [];
	$scope.characteristics = [];

	Telescope.get({},
		function(data) {
			console.log("Received instruments: ");
			console.log(data);
			for(var t = 0; t < data.objects.length; t++) {
				console.log(data.objects[t]);
				$scope.instruments.push({
					name: data.objects[t].name,
					multiSelectGroup: true
				});
				for(var i = 0; i < data.objects[t].instruments.length; i++) {
					$scope.instruments.push({
						name: '<span style="padding-left: 1em;">' + data.objects[t].instruments[i].name + '</span>',
						checked: false,
						value: data.objects[t].instruments[i].name
					});
				}
				$scope.instruments.push({
					multiSelectGroup: false
				});

			}
			console.log("Scope: ");
			console.log($scope);
		});

	Characteristic.get({},
		function(data) {
			console.log("Received characteristics: ");
			console.log(data);
			for(var t = 0; t < data.objects.length; t++) {
				console.log(data.objects[t]);
				$scope.characteristics.push({
					name: '<span style="padding-left: 1em;">' + data.objects[t].name + '</span>',
					checked: false,
					value: data.objects[t].name
				});
			}
			console.log("Scope: ");
			console.log($scope);
		}
	);
	// Function to update dataset using search button
	$scope.update_datasets = function() {
		console.log("Updating datasets");
		// ajax request to api, put filter in the {}
		params = {};
		var selected_instruments = $filter('filter')($scope.instruments, {
			checked: true
		});
		if(selected_instruments.length != 0) {
			params.instrument__in = selected_instruments.map(function(element) {
				return element.value;
			});
		}
		var selected_characteristics = $filter('filter')($scope.characteristics, {
			checked: true
		});
		if(selected_characteristics.length != 0) {
			params.characteristics__in = selected_characteristics.map(function(element) {
				return element.value;
			});
		}


		console.log("Query params");
		console.log(params);
		Dataset.get(params, function(data) {
			$scope.datasets = data.objects;
		});
	};

	$scope.update_datasets();
});
