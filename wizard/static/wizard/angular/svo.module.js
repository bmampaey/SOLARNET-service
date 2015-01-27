var SVOapp = angular.module('SVOapp', [
	'ui.bootstrap',
	'dataset',
	'user_data_selection',
	'swap_lev1',

]);

SVOapp.directive('searchDataset', function(){
	return {
		restrict : 'E',
		scope:{},
		controller : "@"+"Ctrl",
		name:"datasetId",
		templateURL: 'swap_lev1/swap_lev1.html'
	};
});
