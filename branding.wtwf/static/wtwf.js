// Generated by CoffeeScript 1.9.3
(function() {
  var app;

  app = angular.module("Wtwf", []);

  app.controller("MainController", function($sce) {
    var p;
    p = document.location.pathname;
    if (p.length > 1) {
      this.search = p.slice(1);
      this.searchUrl = $sce.trustAsResourceUrl("http://www.google.com/custom?q=" + this.search + "&btnG=Search");
    }
    this.email = location.hostname;
    if (this.email.slice(0, 3) === "www") {
      this.email = this.email.slice(4);
    }
    this.email = "mailto:web2" + (String.fromCharCode("64")) + this.email;
    return this;
  });

}).call(this);
