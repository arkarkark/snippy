# focus a directive when it's first rendered
# alternatively set ark-focus="somePromise" and when the promise is done select everything.
# ark-focus can be an array of promises and boolean values and we'll focus when they're ALL resolved/true
# e.g. ark-focus="[somePromise, thing.visible]"
angular.module('ArkFocus', []).directive('arkFocus', ($q, $timeout) ->
  priority: 2
  scope:
    'arkFocus': '&arkFocus'
  link: (scope, element, attrs) ->
    doFocus = -> $(element).focus()

    scope.$watchCollection('arkFocus()', (newValue) ->
      newValue = [newValue] unless _.isArray(newValue)
      promises = []
      for value, index  in newValue
        if value?.then?
          promises.push(value)
        else
          return unless value
      if promises.length
        # $timeout because the promise will likely update the element.
        $q.all(promises).then(-> $timeout(doFocus))
      else
        doFocus()
    )
    doFocus()
)
