angular.module("SnippySearch").controller("SearchController", (
  $location, $q, $scope, $window, Snip) ->

  @snips = []
  @snipSelected = []
  @allSelected = false
  @searchText = $location.search().for

  @searchChanged = =>
    $location.search("for", @searchText)

  @search = ->
    # TODO(ark) indicate search is happening
    @snips = Snip.query({search: @searchText})
    @busy = @snips.$promise
    @busyMessage = "Searching"

  @update = ->
    console.log("update")

  @delete = (resultsForm) =>
    promises = []
    for selected, index in @snipSelected
      if selected
        promises.push(deleteSnip(@snips[index]))
    @busy = $q.all(promises).then(=> @allSelected = false)
    @busyMessage = "Deleting"

  deleteSnip = (snipToDelete) =>
    snipToDelete.$delete(=>
      for snip, index in @snips
        break if snip.id = snipToDelete.id
      if snip.id == snipToDelete.id
        @snips.splice(index, 1)
        @snipSelected.splice(index, 1)
    )

  @exportString = =>
    selected = _.chain(@snips)
      .filter((s, index) => @snipSelected[index])
      .map((s) -> _.omit(s, "id"))
      .value()
    JSON.stringify(selected, null, 2)

  @exportFileName = =>
    fileName = @searchText || "all"
    # TODO(ark) add in if they searched for private/proxy/promoted
    fileName += ".json"

  @search() if @searchText

  @buttonsEnabled = =>
    !_.some(@snipSelected, (snip) -> snip)

  $scope.$watch((=> @allSelected), (=> @snips.forEach((snip, index) => @snipSelected[index] = @allSelected)))

  @
)
