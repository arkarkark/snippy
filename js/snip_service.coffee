angular.module('Snippy').factory('Snip', ($resource) ->
  new $resource('/admin/api/snip/', {id: '@id'})
)
