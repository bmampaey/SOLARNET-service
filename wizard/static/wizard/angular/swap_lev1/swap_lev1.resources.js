var swap_lev1 = angular.module('swap_lev1');

swap_lev1.factory('MetaData', ['$resource',
	function($resource) {
		return $resource('/api/v1/swap_lev1_meta_data');
	}
]);

swap_lev1.factory('Tag', ['$resource',
	function($resource) {
		return $resource('/api/v1/swap_lev1_tag');
	}
]);
