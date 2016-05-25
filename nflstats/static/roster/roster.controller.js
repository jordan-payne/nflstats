(function() {
  'use strict';

  angular
    .module('nflstats')
    .controller('RosterController', RosterController);

  RosterController.$inject = ['$http', 'nfl_teams'];

  function RosterController($http, nfl_teams) {
    var vm = this;
    vm.gridOptions = {};
    vm.teams = nfl_teams;
    vm.gridOptions.columnDefs = [
      { name:'last_name', width:120},
      { name:'first_name', width:120},
      { name:'position', width:120},
      { name:'weight', width:120},
      { name:'height', width:120},
      { name:'years_pro', width:120},
      { name:'college', width:120}
    ];

    vm.getTeamRoster = function(team) {
      $http.post('/get_team_roster', team)
        .then(function successCallback(response) {
          vm.result = response.data;
          vm.gridOptions.data = response.data;
      }, function errorCallback(response) {
          vm.result = response.data;
      });
    };

  }
})();
