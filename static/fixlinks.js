<!--
// Copyright 2007 Alex K (wtwf.com) All Rights Reserved

// I forget where I got this from, It's not mine though, sorry...
if (!String.prototype.endsWith) {
  String.prototype.endsWith = function(suffix) {
    var startPos = this.length - suffix.length;
    if (startPos < 0) {
      return false;
    }
    return (this.lastIndexOf(suffix, startPos) == startPos);
  };
}

function openLinkPossiblyInNewWindow(link) {
  if (!(link.protocol == 'http:' ||
        link.protocol == 'https:' ||
        link.protocol == 'ftp:')) {
    // we only handle https?|ftp anything else let the browser handle it
    return true;
  }
  if ((link.target && link.target != '_self') ||
      link.hostname != document.location.hostname ||
      link.pathname.toLowerCase().endsWith('.jpg') ||
      link.pathname.toLowerCase().endsWith('.gif') ||
      link.pathname.toLowerCase().endsWith('.png') ||
      false) {
    var newlink = link.href.toString();
    if (link.hostname != document.location.hostname) {
      // we want to use hide behind for off site links
      if (newlink.indexOf('?') == -1 &&
          newlink.indexOf('#') == -1 &&
          !newlink.endsWith('.js')) {
        newlink = 'http://app.wtwf.com/r/' + newlink;
      }
    }
    if (link.target) {
      window.open(newlink, link.target);
    } else {
      window.open(newlink);
    }
  } else {
    document.location.href = link.href;
  }
  return false;
}

/** Get a closure that calls a function and then returns the value
    from calling our go function
*/
function getClosure(func) {
  return function() {
    if (func) {
      if (!func()) {
        return false;
      }
    }
    return openLinkPossiblyInNewWindow(this);
  };
}

/** Go through a page and make all urls 'hidden' so that they won't
    leak refereres. Also make it so that they open off site links in a
    new window.
*/
function anonymizeurls() {
  var pageLinks;
  if (document.getElementsByTagName) {
    pageLinks = document.getElementsByTagName('a');
  } else {
    pageLinks = document.links;
  }
  for (var i = 0; i < pageLinks.length; i++) {
    pageLinks[i].onclick = getClosure(pageLinks[i].onclick);
  }
}

// from http://simon.incutio.com/archive/2004/05/26/addLoadEvent
// Usage examples....
// addLoadEvent(nameOfSomeFunctionToRunOnPageLoad);
// addLoadEvent(function() {
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

addLoadEvent(anonymizeurls);
// -->
