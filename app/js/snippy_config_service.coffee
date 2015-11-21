angular.module("Snippy").factory("SnippyConfig", ($resource) ->
  new $resource("/admin/api/snippyconfig/")
)
