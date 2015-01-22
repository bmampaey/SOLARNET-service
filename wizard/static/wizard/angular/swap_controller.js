var swapApp = angular.module('swapApp', ['ngResource', 'multi-select', 'ui.bootstrap.datetimepicker']);

swapApp.factory('SwapMetaData', ['$resource',
	function($resource) {
		return $resource('http://benjmam-pc:8000/api/v1/swap_meta_data');
	}
]);

swapApp.factory('SwapTag', ['$resource',
	function($resource) {
		return $resource('http://benjmam-pc:8000/api/v1/swap_tag');
	}
]);

swapApp.controller('swapController', function($scope, $timeout, $filter, SwapMetaData, SwapTag) {
	
	// debugging hack 
	window.MY_SCOPE = $scope;
	// load tags
	$scope.tags = [];

	SwapTag.get({},
		function(data) {
			console.log("Received tags: ");
			console.log(data);
			for(var t = 0; t < data.objects.length; t++) {
				console.log(data.objects[t]);
				$scope.tags.push({
					name: '<span style="padding-left: 1em;">' + data.objects[t].name + '</span>',
					checked: false,
					value: data.objects[t].name
				});
			}
			console.log("Scope: ");
			console.log($scope);
		}
	);
	
	// Function to update meta_data using search button
	$scope.update_meta_datas = function() {
		console.log("Updating meta_datas");
		// ajax request to api, put filter in the {}
		params = {};
		var selected_tags = $filter('filter')($scope.tags, {
			checked: true
		});
		if(selected_tags.length != 0) {
			params.tags__in = selected_tags.map(function(element) {
				return element.value;
			});
		}
		console.log("Query params");
		console.log(params);
		SwapMetaData.get(params, function(data) {
			$scope.meta_datas = data.objects.map(function(meta_data){meta_data.tags = meta_data.tags.map(function(tag){return tag.name}); return meta_data});
		});
	};

	$scope.update_meta_datas();
});