app = angular.module("SnippyAdminController", []).controller "AdminController", (
  $http
  $window
  SnippyConfig
) ->
  SnippyConfig.get().$promise.then((config) =>
    @domain = config.baseUrl.split("/")[2]
  )

  @addWellKnown = (location, fact) =>
    return unless fact
    @lastAddedFact = ""
    @busy = $http.post("/admin/api/wellknown", location: location, fact: fact)
    @busy.then((data) =>
      @lastAddedFact = fact
    ).catch((data) ->
      alert("That didn't work!", data)
      console.error("error:", data)
    ).finally ->
      @busyMessage = ""
      @message = "done saving fact"

    @busyMessage = "Saving Fact"

  @testWellKnown = (fact) ->
    url = fact.split(".")[0]
    $window.open("/.well-known/acme-challenge/#{url}", "_blank")
    true # so we don't return a window

  @busyMessage = "Please wait"
  @busy = null
  @message = ""



  @
