angular.module('SnippySearch').controller('SearchController', (
  $location, $scope, $window, Snip) ->

  @snips = []
  @snipSelected = []
  @allSelected = false
  @searchText = $location.search().for

  @searchChanged = =>
    $location.search('for', @searchText)

  @search = ->
    # TODO(ark) indicate search is happening
    @snips = Snip.query({search: @searchText})

  @update = ->
    console.log('update')

  @delete = ->
    console.log('delete')

  @export = =>
    params =
      search: @searchText
      download: true
    url = "/admin/api/snip?#{$.param(params)}"
    console.log(url)
    $window.open(url, '_self')
    url # return something that's not $window

  @search() if @searchText

  @buttonsEnabled = =>
    !_.some(@snipSelected, (snip) -> snip)

  $scope.$watch((=> @allSelected), (=> @snips.forEach((snip, index) => @snipSelected[index] = @allSelected)))

  @
)
