# ark-user - shows the currently logged in user
angular.module('Snippy').directive('arkUser', ->
  templateUrl: '/static/html/user/user.html'
  controller: 'UserController'
  controllerAs: 'userController'
  scope:
    'forceLogin': '@arkAttrForceLogin'
)
