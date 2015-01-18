angular.module('SnippyEdit', []).controller('EditController', (
  $location, $scope, Snip) ->

  @originalId = $location.search().id
  Snip.query({keyword: @originalId}, (snips) =>
    @snip = snips?[0] || {}
    @original = angular.copy(@snip)
  )

  @keywordChanged = =>
    $location.search('id', @snip.keyword)

  @save = (form) =>
    console.log('save', form)
    if @snip.keyword != @original.keyword
      # TODO(ark): ask to save or replace?
      @snip.$save()
    else
      @snip.$save()


  @delete = (form) =>
    console.log('delete', form)
    if confirm('are you sure you want to delete?')
      @snip.$delete()

  @
)
