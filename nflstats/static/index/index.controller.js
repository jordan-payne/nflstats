(function() {
  'use strict';

  angular
    .module('nflstats')
    .controller('IndexController', IndexController);

    IndexController.$inject = ['$http']
    function IndexController($http) {
      var vm = this;
      var names_with_ids = undefined;

      (function() {
        $http.post('/get_all_names')
          .then(function successCallback(response) {
            names_with_ids = response.data;
            vm.names = _.map(response.data, 'name');
          }, function errorCallback(response) {
            vm.error = response.data;
          })
      })();
      vm.selected = undefined;

      vm.getPlayer = function(name) {
        var id = _.find(names_with_ids, {name: name}).id;
        $http.post('/get_player_from_id', {'id': id})
          .then(function successCallback(response) {
            vm.player = response.data;
            console.log(vm.player);
          }, function errorCallback(response) {
            vm.error = response.data;
          });
      }
    }
})();
