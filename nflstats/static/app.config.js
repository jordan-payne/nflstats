(function() {
  'use strict';

  angular
    .module('nflstats')
    .config(configure);

  configure.$inject = ['$urlRouterProvider', '$stateProvider'];

  function configure($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/')

    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'index.html',
        controller: 'IndexController as index'
      })
      .state('roster', {
        url: '/roster',
        templateUrl: 'roster/roster.html',
        controller: 'RosterController as roster'
      })
      .state('player_stats', {
        url: '/player_stats',
        templateUrl: 'player_stats/player_stats.html',
        controller: 'PlayerStatsController as players'
      });
  }

})();
