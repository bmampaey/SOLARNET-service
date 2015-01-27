var dataset = angular.module('dataset');

dataset.factory('Dataset', ['$resource',
	function($resource) {
		return $resource('/api/v1/dataset');
	}
]);

dataset.factory('Telescope', ['$resource',
	function($resource) {
		return $resource('/api/v1/telescope');
	}
]);

dataset.factory('Characteristic', ['$resource',
	function($resource) {
		return $resource('/api/v1/characteristic');
	}
]);
