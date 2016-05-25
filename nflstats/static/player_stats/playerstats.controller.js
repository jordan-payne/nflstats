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
      { field:'year', width:120},
      { displayName: 'Passing TD', name:'passing_tds', width:120},
      { displayName: 'Passing Yds', name:'passing_yds', width:120},
      { displayName: 'Cmp', name:'passing_cmp', width:120},
      { displayName: 'Pass Att', name:'passing_att', width:120},
      { displayName: 'Rushing TD', name:'rushing_tds', width:120},
      { displayName: 'Rushing Yds', name:'rushing_yds', width:120}
    ];

    vm.getPlayer = function(player) {
      $http.post('/get_player', player)
        .then(function successCallback(response) {
          vm.player = response.data;
      }, function errorCallback(response) {
          vm.player = response.data;
      });
      $http.post('/get_player_all_time_stats_by_year', player)
        .then(function successCallback(response) {
          vm.gridOptions.data = _.values(response.data)
      }, function errorCallback(response) {
          vm.stats = response.data;
      });
    };
  }

})();
