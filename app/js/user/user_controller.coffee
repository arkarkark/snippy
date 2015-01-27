angular.module('Snippy').controller('UserController', (
  $window, $rootScope, $scope, User) ->

  $rootScope.currentUser = $scope.currentUser = User.get({}, (user) ->
    $window.open(user.login, '_self') if user.login && $scope.forceLogin
  )

  @
)
