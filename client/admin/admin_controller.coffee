app = angular.module("SnippyAdminController", []).controller("AdminController", (
  $http
  $window
  SnippyConfig
) ->
  SnippyConfig.get().$promise.then((config) =>
    @domain = config.baseUrl.split("/")[2]
  )

  @addWellKnown = (fact) =>
    return unless fact
    @lastAddedFact = ""
    @busy = $http.post("/admin/api/wellknown", fact: fact)
    @busy.then((data) =>
        @lastAddedFact = fact
      ).catch((data) ->
        alert("That didn't work!", data)
        console.error("error:", data)
      )
    @busyMessage = "Saving Fact"
    @message = "done saving fact"

  @testWellKnown = (fact) ->
    url = fact.split(".")[0]
    $window.open("/.well-known/acme-challenge/#{url}", "_blank")
    true # so we don't return a window

  @busyMessage = "Please wait"
  @busy = null
  @message = ""



  @
)
