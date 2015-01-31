# select everything in a input when it gets focus
angular.module('SelectAll', []).directive('arkSelectAll', ->
  priority: 1
  link: (scope, element) ->
    el = $(element)
    el.focus(-> el.select())
)
