var swapApp = angular.module('swapApp', ['ngResource', 'multi-select', 'ui.bootstrap']);

swapApp.factory('MetaData', ['$resource',
	function($resource) {
		return $resource('/api/v1/swap_meta_data');
	}
]);

swapApp.factory('Tag', ['$resource',
	function($resource) {
		return $resource('/api/v1/swap_tag');
	}
]);

swapApp.controller('controller', function($scope, $filter, MetaData, Tag) {
	
	// debugging hack 
	window.MY_SCOPE = $scope;
	// load tags
	$scope.tags = [];

	Tag.get({},
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
		var params = {};
		var selected_tags = $filter('filter')($scope.tags, {
			checked: true
		});
		if(selected_tags.length != 0) {
			params.tags__in = selected_tags.map(function(element) {
				return element.value;
			});
		}
		if($scope.start_date)
		{
			params.date_obs__gte = $scope.start_date.toISOString();
		}
		
		if($scope.end_date)
		{
			params.date_obs__lt = $scope.end_date.toISOString();
		}
		console.log("Query params");
		console.log(params);
		MetaData.get(params, function(data) {
			console.log("Received data", data)
			$scope.meta_datas = data.objects.map(function(meta_data){meta_data.tags = meta_data.tags.map(function(tag){return tag.name}); return meta_data});
			$scope.search_params = params;
			$scope.search_params.offset = 0;
			$scope.page = 0;
			$scope.last_page = data.meta.total_count / data.meta.limit;
			$scope.search_params.limit = data.meta.limit;
		});
	};



	$scope.update_meta_datas();

	$scope.load_page = function(page_number) {
		var params = $scope.search_params;
		params.offset = page_number * $scope.search_params.limit;
		console.log("Load page", page_number, "with params", params);
		MetaData.get(params, function(data) {
			console.log("Received data", data)
			$scope.meta_datas = data.objects.map(function(meta_data){meta_data.tags = meta_data.tags.map(function(tag){return tag.name}); return meta_data});
			console.log("New meta-data:", $scope.meta_datas);
			$scope.search_params = params;
			$scope.page = page_number;
		});
	};
	
	$scope.date_pickers = {'start_date': false, 'end_date': false};
	$scope.date_format = 'yyyy-MM-dd 00:00:00';
	$scope.open_date_picker = function($event, date_picker) {
		$event.preventDefault();
		$event.stopPropagation();
		$scope.date_pickers[date_picker] = !$scope.date_pickers[date_picker];
		console.log("Opening date picker" , date_picker, $scope.date_pickers[date_picker]);
	};
	window.my_scope = $scope;
});
