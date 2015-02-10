# ark-download
angular.module('Download', []).directive('arkDownload', ->
  restrict: 'A'
  scope:
    value: '&arkDownload'
    fileName: '@arkAttrFileName'
    mimeType: '@arkAttrMimeType'
  link: (scope, element) ->
    element.bind('click', ->
      el = angular.element('<a>')[0]
      el.href = URL.createObjectURL(new Blob([scope.value()], {type: scope.mimeType}))
      el.download = scope.fileName
      el.click()
    )
)
