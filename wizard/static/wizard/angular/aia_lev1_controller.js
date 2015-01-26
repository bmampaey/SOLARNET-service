var aiaLev1App = angular.module('aiaLev1App', ['ngResource', 'multi-select']);

aiaLev1App.factory('AIALev1MetaData', ['$resource',
	function($resource) {
		return $resource('/api/v1/aia_lev1_meta_data');
	}
]);

aiaLev1App.factory('AIALev1Tag', ['$resource',
	function($resource) {
		return $resource('/api/v1/aia_lev1_tag');
	}
]);

aiaLev1App.controller('aiaLev1Controller', function($scope, $timeout, $filter, AIALev1MetaData, AIALev1Tag) {
	
	// debugging hack 
	window.MY_SCOPE = $scope;
	// load tags
	$scope.tags = [];

	AIALev1Tag.get({},
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
		AIALev1MetaData.get(params, function(data) {
			$scope.meta_datas = data.objects;
		});
	};

	$scope.update_meta_datas();
});
