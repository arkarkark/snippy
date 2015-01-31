# focus a directive when it's first rendered
# alternatively set ark-focus="somePromise" and when the promise is done select everything.
angular.module('Focus', []).directive('arkFocus', ($timeout) ->
  priority: 2
  scope:
    'arkFocus': '=?arkFocus'
  link: (scope, element, attrs) ->
    doFocus = -> $(element).focus()

    if attrs.arkFocus?
      scope.$watch('arkFocus', (newValue) ->
        if newValue?.then?
          newValue.then(-> $timeout(doFocus)) # $timeout because the promise will likely update the element.
      )
    doFocus()
)
