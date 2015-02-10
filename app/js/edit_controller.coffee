angular.module('SnippyEdit', []).controller('EditController', (
  $location, $scope, $timeout, Snip, QrService) ->
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
    if @snip.keyword != @originalKeyword
      existing = Snip.query({keyword: @snip.keyword}).$promise
      ans = confirm("You modified the keyword from '#{@snip.keyword}' to '#{@originalKeyword}'\n" +
                    "Select Cancel to create a new snip leaving '#{@originalKeyword}' alone.\n" +
                    "Select OK to rename the '#{@originalKeyword}' snip\n")
      delete @snip.id unless ans
      @busyMessage = "Checking to see if '#{@snip.keyword}' already exists"
      @busy = existing
      @busy.then((snips) =>
        if snips.length
          if confirm("'#{@snip.keyword}' snip exists! Do you want to overwrite it?")
            @snip.id = snips[0].id
            @busyMessage = 'Saving'
            @busy = @snip.$save()
            @busy.then(=> @setMessage('Overwritten'))
          else
            @busy = null
        else
          @busyMessage = 'Saving'
          @busy = @snip.$save()
          @busy.then(=> @setMessage(if ans then 'Renamed' else 'Created'))
        @busy?.then(=>
          @originalKeyword = @snip.keyword
          @original = angular.copy(@snip)
        )
      )
    else
      @busyMessage = 'Saving'
      @busy = @snip.$save()
      @busy.then(=> @setMessage('Saved'))

  @setMessage = (msg) =>
    @message = msg
    console.info(msg)
    $timeout(
      => @message = ''
      1000
    )

  @delete = (form) =>
    console.log('delete', form)
    if confirm("Are you sure you want to delete '#{@snip.keyword}'?")
      @snip.$delete(=> delete @snip.id)

  @getUrl = =>
    'http://wtwf.com/' + @snip?.keyword

  @exportString = =>
    JSON.stringify(_.omit(@snip, 'id') || '', null, 2)


  # TODO(ark) handle url= being in the $location.search() that means we have a new setting.

  @
)
