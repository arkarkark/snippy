angular.module("Snippy").factory("User", ($resource) ->
  new $resource("/admin/api/user")
)
