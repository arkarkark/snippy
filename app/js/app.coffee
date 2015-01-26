# Hello world
#
angular.module('SnippySearch', [])

app = angular.module('Snippy', [
  'SnippyEdit'
  'SnippySearch'
  'QrCode'
  'ui.router'
  'ngResource'
  'monospaced.qrcode'
  'ui.bootstrap'
  'cgBusy'
]).config(($locationProvider, $stateProvider, $urlRouterProvider) ->
  $locationProvider.html5Mode(true)
  $urlRouterProvider.otherwise('/admin/')

  $stateProvider.state('home',
    url: '/admin/'
    templateUrl: '/static/html/list.html'
  ).state('Edit',
    url: '/admin/edit/'
    templateUrl: '/static/html/edit.html'
    controller: 'EditController as editController'
    reloadOnSearch: false
  ).state('Search',
    url: '/admin/search/'
    templateUrl: '/static/html/search.html'
    controller: 'SearchController as searchController'
    reloadOnSearch: false
  ).state('Import',
    url: '/admin/import/'
    templateUrl: '/static/html/import.html'
  )
).run(($rootScope, $state, $stateParams) ->
  $rootScope.$state = $state
  $rootScope.$stateParams = $stateParams
)
