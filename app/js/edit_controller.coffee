angular.module('SnippyEdit', []).controller('EditController', (
  $location, $scope, Snip, QrService) ->

  @qrSettings = =>
    QrService.settings(@getUrl())

  @originalKeyword = $location.search().keyword || ''
  Snip.query({keyword: @originalKeyword}, (snips) =>
    @snip = snips?[0] || new Snip({keyword: @originalKeyword, id: 'new'})
    @original = angular.copy(@snip)
  )

  @keywordChanged = =>
    $location.search('keyword', @snip.keyword)

  @save = (form) =>
    # TODO(ark) indicate saving is happening
    # TODO(ark) handle errors
    if @snip.keyword != @original.keyword
      # TODO(ark): ask to save or replace?
      @snip.$save()
    else
      @snip.$save()


  @delete = (form) =>
    console.log('delete', form)
    if confirm("Are you sure you want to delete '#{@snip.keyword}'?")
      @snip.$delete(=> delete @snip.id)

  @getUrl = =>
    'http://wtwf.com/' + @snip?.keyword

  # TODO(ark) handle url= being in the $location.search() that means we have a new setting.

  @
)
