angular.module("SnippyEdit", []).controller("EditController", (
  $http
  $location
  $sce
  $scope
  $timeout
  $window
  Snip
  QrService
  SnippyConfig
) ->
  @qrSettings = =>
    QrService.settings(@getUrl())

  @addThisIp = =>
    url = $sce.trustAsResourceUrl('https://api.ipify.org?format=jsonp')
    $http.jsonp(url, jsonpCallbackParam: 'callback').then (response) =>
      @snip.ip_restrict = response.data.ip

  @originalKeyword = $location.search().keyword || ""
  @snip = Snip.query({keyword: @originalKeyword}, (snips) =>
    @snip = snips?[0] || new Snip({keyword: @originalKeyword, id: ""})
    @original = angular.copy(@snip)
    @snipUrl = @getUrl()
    newUrl = $location.search().url
    if newUrl && @original.url
      @snip.url = newUrl
      @oldUrl = @original.url
      @message = "A snip with that name already exists. Click Save to update with this new url."
  )

  @config = SnippyConfig.get()

  @keywordChanged = =>
    $location.search("keyword", @snip.keyword)
    @snipUrl = @getUrl()

  @snipChanged = =>
    newKeyword = @snipUrl[@getBaseUrl().length...]
    if newKeyword && newKeyword != @snip?.keyword
      @snip.keyword = newKeyword
      @keywordChanged()
    @snipUrl = @getUrl()

  @getBaseUrl = =>
    @config.baseUrl || "#{$location.absUrl().split("/").splice(0, 3).join("/")}/"

  @getUrl = =>
    if @snip?.keyword then @getBaseUrl() + @snip?.keyword else ""

  @restoreOldUrl = =>
    [@snip.url, @oldUrl] = [@oldUrl, @snip.url]

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
            @busyMessage = "Saving"
            @busy = @snip.$save()
            @busy.then(=> @setMessage("Overwritten"))
          else
            @busy = null
        else
          @busyMessage = "Saving"
          @busy = @snip.$save()
          @busy.then(=> @setMessage(if ans then "Renamed" else "Created"))
        @busy?.then(=>
          @originalKeyword = @snip.keyword
          @original = angular.copy(@snip)
        )
      )
    else
      @busyMessage = "Saving"
      @busy = @snip.$save()
      @busy.then(=> @setMessage("Saved"))

  @setMessage = (msg) =>
    @message = msg
    console.info(msg)
    $timeout(
      => @message = ""
      1000
    )

  @delete = (form) =>
    console.log("delete", form)
    if confirm("Are you sure you want to delete '#{@snip.keyword}'?")
      @snip.$delete(=> delete @snip.id)

  @exportString = =>
    JSON.stringify(_.omit(@snip, "id") || "", null, 2)

  $scope.$on("arkOpenUrl", => $window.open("#{@getBaseUrl()}/r/#{encodeURIComponent(@getUrl())}", "_self"))

  @
)
