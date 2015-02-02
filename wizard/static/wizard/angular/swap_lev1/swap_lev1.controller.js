var swap_lev1 = angular.module('swap_lev1');

swap_lev1.controller('swap_lev1Ctrl', function($scope, $filter, MetaData, Tag) {

	$scope.date_pickers = {'start_date': false, 'end_date': false};
	$scope.date_format = 'yyyy-MM-dd 00:00:00';
	$scope.tags = [];
	$scope.items_per_page = 20;

	// Load tags
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

	// Function to load meta-data
	$scope.load_meta_datas = function(page, search_params) {
		
		search_params = (typeof search_params === "undefined") ? angular.copy($scope.search_params) : search_params;
		page = (typeof page === "undefined") ? 1 : page;
		
		search_params.offset = (page - 1) * $scope.items_per_page;
		search_params.limit = $scope.items_per_page;
		
		console.log("Load page", page, "with params", search_params);
		
		MetaData.get(search_params, function(data) {
			console.log("Received data", data)
			$scope.meta_datas = data.objects.map(function(meta_data){meta_data.tags = meta_data.tags.map(function(tag){return tag.name}); return meta_data});
			$scope.meta_meta_datas = data.meta;
			$scope.search_params = search_params;
			$scope.page = page;
			$scope.items_per_page = data.meta.limit;
		});
	};

	// Function to search for meta-datas
	$scope.search_meta_datas = function() {
		console.log("Search meta-datas");
		var search_params = {
			limit: $scope.items_per_page,
		};
		
		var selected_tags = $filter('filter')($scope.tags, {
			checked: true
		});
		
		if(selected_tags.length != 0) {
			search_params.tags__in = selected_tags.map(function(element) {
				return element.value;
			});
		}
		
		if($scope.start_date)
		{
			var date = angular.copy($scope.start_date);
			date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
			search_params.date_obs__gte = date.toISOString();
		}
		
		if($scope.end_date)
		{
			var date = angular.copy($scope.end_date);
			date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
			search_params.date_obs__lt = date.toISOString();
		}
		
		console.log("Search params");
		console.log(search_params);
		$scope.load_meta_datas(1, search_params);
	};

	// Function to open a date picker
	$scope.open_date_picker = function($event, date_picker) {
		$event.preventDefault();
		$event.stopPropagation();
		$scope.date_pickers[date_picker] = !$scope.date_pickers[date_picker];
		console.log("Opening date picker" , date_picker, $scope.date_pickers[date_picker]);
	};

	// Load first page of meta data
	$scope.search_meta_datas();
	
	console.log("swap_lev1Ctrl scope", $scope);
});
