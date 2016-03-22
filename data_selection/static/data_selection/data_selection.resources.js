var DataSelectionApp = angular.module('DataSelectionApp');

DataSelectionApp.factory('DataSelection', ['SVO_URL', '$resource',
	function(SVO_URL, $resource) {
		return $resource(SVO_URL + 'user_data_selection');
	}
]);
