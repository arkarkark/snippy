app = angular.module("Wtwf", [])

app.controller("MainController", ($sce) ->
  p = document.location.pathname;
  if p.length > 1
    @search = p[1..]
    @searchUrl = $sce.trustAsResourceUrl("http://www.google.com/custom?q=#{@search}&btnG=Search")

  @email = location.hostname
  @email = @email[4..] if @email[0..2] == "www"
  @email = "mailto:web2#{String.fromCharCode("64")}#{@email}"

  @
)
