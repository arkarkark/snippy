# Hello world
#

app = angular.module('Snippy', [
  'ui.router'
]).config(($locationProvider, $stateProvider, $urlRouterProvider) ->
  $locationProvider.html5Mode(true)
  $urlRouterProvider.otherwise('/admin/')

  $stateProvider.state('home',
    url: '/admin/'
    templateUrl: '/static/html/list.html'
  ).state('Add',
    url: '/admin/add/'
    templateUrl: '/static/html/add.html'
  )
).run(($rootScope, $state, $stateParams) ->
  $rootScope.$state = $state
  $rootScope.$stateParams = $stateParams
  console.log('snippy is inited')
)
