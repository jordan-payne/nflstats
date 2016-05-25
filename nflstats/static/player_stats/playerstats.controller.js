(function() {
  'use strict';

  angular
    .module('nflstats')
    .controller('PlayerStatsController', PlayerStatsController);

  PlayerStatsController.$inject = ['$http', 'nfl_teams'];

  function PlayerStatsController($http, nfl_teams) {
    var vm = this;
    vm.teams = nfl_teams;
    vm.gridOptions = {};
    vm.gridOptions.columnDefs = [
      { name:'last_name', width:120},
      { name:'first_name', width:120},
      { name:'position', width:120},
      { name:'weight', width:120},
      { name:'height', width:120},
      { name:'years_pro', width:120},
      { name:'college', width:120}
    ];

    vm.getPlayer = function(player) {
      $http.post('/get_player', player)
        .then(function successCallback(response) {
          vm.player = response.data;
      }, function errorCallback(response) {
          vm.player = response.data;
      });
      $http.post('/get_player_all_time_stats', player)
        .then(function successCallback(response) {
          vm.stats = response.data;
      }, function errorCallback(response) {
          vm.stats = response.data;
      });
    };
  }

})();
