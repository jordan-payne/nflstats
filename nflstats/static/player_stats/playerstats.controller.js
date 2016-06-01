(function() {
  'use strict';

  angular
    .module('nflstats')
    .controller('PlayerStatsController', PlayerStatsController);

  PlayerStatsController.$inject = ['$http', 'nfl_teams'];

  function PlayerStatsController($http, nfl_teams) {
    var vm = this;
    vm.teams = nfl_teams;
    vm.rushingGridOptions = {};
    vm.passingGridOptions = {};
    vm.passingGridOptions.columnDefs = [
      { name:'year', width:60},
      { displayName: 'Tds', name:'passing_tds'},
      { displayName: 'Twopta', name: 'passing_twopta'},
      { displayName: 'Twoptm', name: 'passing_twoptm'},
      { displayName: 'Yds', name:'passing_yds'},
      { displayName: 'Comp', name:'passing_cmp'},
      { displayName: 'Att', name:'passing_att'},
      { displayName: 'Air Yds', name:'passing_cmp_air_yds'},
      { displayName: 'Incmp', name: 'passing_incmp'},
      { displayName: 'Incmp Air Yds', name: 'passing_incmp_air_yds'},
      { displayName: 'Int', name: 'passing_int'},
      { displayName: 'Sck', name: 'passing_sk'},
      { displayName: 'SckY', name: 'passing_sk_yds'}
    ];

    vm.rushingGridOptions.columnDefs = [
      { name:'year', width:60},
      { displayName: 'Tds', name: 'rushing_tds'},
      { displayName: 'Twopta', name: 'rushing_twopta'},
      { displayName: 'Twoptm', name: 'rushing_twoptm'},
      { displayName: 'Yds', name: 'rushing_yds'},
      { displayName: 'Att', name: 'rushing_att'}
    ]

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
        }, function errorCallback(response) {
          vm.error = response.data;
        });
      $http.post('/get_player_all_time_stats_by_year', {'id': id})
        .then(function successCallback(response) {
          vm.passingGridOptions.data = vm.rushingGridOptions.data = response.data;
        }, function errorCallback(response) {
          vm.error = response.data;
        });
    }
  }

})();
