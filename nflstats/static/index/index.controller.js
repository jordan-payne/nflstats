(function() {
  'use strict';

  angular
    .module('nflstats')
    .controller('IndexController', IndexController);

    IndexController.$inject = ['$http']
    function IndexController($http) {
      var vm = this;

      (function() {
        $http.post('/get_all_names')
          .then(function successCallback(response) {
            vm.names = _.map(response.data, 'full_name');
          }, function errorCallback(response) {
            vm.error = response.data;
          })
      })();
      vm.selected = undefined;

    }
})();
