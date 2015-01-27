var user_data_selection = angular.module('user_data_selection');

user_data_selection.factory('UserSelection', ['$resource',
	function($resource) {
		return $resource('/api/v1/user_data_selection/?user=bmampaey');
	}
]);
