angular.module('SnippySearch').controller('SearchController', (
  $location, $q, $scope, $window, Snip) ->

  @snips = []
  @snipSelected = []
  @allSelected = false
  @searchText = $location.search().for

  @searchChanged = =>
    $location.search('for', @searchText)

  @search = ->
    # TODO(ark) indicate search is happening
    @snips = Snip.query({search: @searchText})
    @busy = @snips.$promise
    @busyMessage = 'Searching'

  @update = ->
    console.log('update')

  @delete = (resultsForm) =>
    promises = []
    for selected, index in @snipSelected
      if selected
        promises.push(deleteSnip(@snips[index]))
    @busy = $q.all(promises).then(=> @allSelected = false)
    @busyMessage = 'Deleting'

  deleteSnip = (snipToDelete) =>
    snipToDelete.$delete(=>
      for snip, index in @snips
        break if snip.id = snipToDelete.id
      if snip.id == snipToDelete.id
        @snips.splice(index, 1)
        @snipSelected.splice(index, 1)
    )

  @export = =>
    # TODO(ark) we have the data just build use URL.createObjectURL and download that
    params =
      search: @searchText
      download: true
    url = "/admin/api/snip?#{$.param(params)}"
    $window.open(url, '_self')
    url # return something that's not $window

  @search() if @searchText

  @buttonsEnabled = =>
    !_.some(@snipSelected, (snip) -> snip)

  $scope.$watch((=> @allSelected), (=> @snips.forEach((snip, index) => @snipSelected[index] = @allSelected)))

  @
)
