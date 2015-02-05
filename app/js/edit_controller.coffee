angular.module('SnippyEdit', []).controller('EditController', (
  $location, $scope, Snip, QrService) ->
  @qrSettings = =>
    QrService.settings(@getUrl())

  @originalKeyword = $location.search().keyword || ''
  @snip = Snip.query({keyword: @originalKeyword}, (snips) =>
    @snip = snips?[0] || new Snip({keyword: @originalKeyword, id: ''})
    @original = angular.copy(@snip)
  )

  @keywordChanged = =>
    $location.search('keyword', @snip.keyword)

  @snipUrl = =>
    if @snip.keyword then "#{$location.absUrl().split('/').splice(0,3).join('/')}/#{@snip.keyword}" else ''

  @swapUrlAltUrl = =>
    [@snip.url, @snip.alt_url] = [@snip.alt_url, @snip.url]

  @save = (form) =>
    # TODO(ark) handle errors
    if @snip.keyword != @original.keyword
      # TODO(ark): ask to save or replace?
      @busy = @snip.$save()
    else
      @busy = @snip.$save()
    @busyMessage = 'Saving'

  @delete = (form) =>
    console.log('delete', form)
    if confirm("Are you sure you want to delete '#{@snip.keyword}'?")
      @snip.$delete(=> delete @snip.id)

  @getUrl = =>
    'http://wtwf.com/' + @snip?.keyword

  # TODO(ark) handle url= being in the $location.search() that means we have a new setting.

  @
)
