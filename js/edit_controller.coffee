angular.module('SnippyEdit', []).controller('EditController', (
  $location, $scope, $stateParams, $state, Snip) ->
  console.log('EditController', $stateParams.id)

  @showIt = =>
    console.log($stateParams.id, $state.params.id, $location.search().id)
    console.log(@snip)

  @originalId = $location.search().id
  Snip.query({keyword: @originalId}, (snips) =>
    @snip = snips?[0] || {}
  )

  @moveIt = ->
    console.log('move it')
    $location.search('id', 'hshdrehrehre')

  @keywordChanged = =>
    $location.search('id', @snip.keyword)


  @save = =>
    @snip.$save()

  @
)
