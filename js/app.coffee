# Hello world
#

app = angular.module('Snippy', [
  'SnippyEdit'
  'ui.router'
  'ngResource'
]).config(($locationProvider, $stateProvider, $urlRouterProvider) ->
  $locationProvider.html5Mode(true)
  $urlRouterProvider.otherwise('/admin/')

  $stateProvider.state('home',
    url: '/admin/'
    templateUrl: '/static/html/list.html'
  ).state('Edit',
    url: '/admin/edit/?:id'
    templateUrl: '/static/html/edit.html'
    controller: 'EditController as editController'
    reloadOnSearch: false
  )
).run(($rootScope, $state, $stateParams) ->
  $rootScope.$state = $state
  $rootScope.$stateParams = $stateParams
  console.log('snippy is inited')
)
