angular.module('SnippySearch').controller('SearchController', (
  $location, $scope, Snip) ->

  @snips = []
  @snipSelected = []
  @searchText = $location.search().for

  @searchChanged = =>
    $location.search('for', @searchText)
    if @searchText.length > 3
      @search()

  @search = ->
    @snips = Snip.query({search: @searchText})

  @update = ->
    console.log('update')

  @delete = ->
    console.log('delete')

  @search() if @searchText

  @
)
