app = angular.module('SnippyAdminController', []).controller('AdminController', (
  $http
  $window
  SnippyConfig
) ->
  SnippyConfig.get().$promise.then((config) =>
    @domain = config.baseUrl.split("/")[2]
  )

  @addWellKnown = (fact) ->
    console.log('Adding well known fact:', fact)
    return unless fact
    @busy = $http.post('/admin/api/wellknown', fact: fact)
      .then((data) ->
        console.log('success:', data)
      ).catch((data) ->
        console.log('error:', data)
      )

    @busyMessage = 'Saving Fact'
    @message = 'done saving fact'

  @testWellKnown = (fact) ->
    url = fact.split(".")[0]
    console.log(url)
    $window.open("/.well-known/acme-challenge/#{url}", "_blank")

  @busyMessage = 'Please wait'
  @busy = null
  @message = ''



  @
)
