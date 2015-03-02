# ark-key-broadcast will broadcast a message when a certain keyboard combo is pressed.
# It's kind of like hotkeys, but works on an element which sometimes hotkeys cannot catch.
# usage:
# <input ark-key-broadcast="{'mod+return': 'arkDoThing', 'mod+shift+return': 'arkReallyDoThing'}">
# key descriptions are the same as hotkeys
angular.module('ArkKeyBroadcast', []).directive('arkKeyBroadcast', ($rootScope) ->
  restrict: 'A'
  priority: 2
  link: (scope, element, attrs) ->
    # some of these are from mousetrap.js
    _SPECIAL_ALIASES = {
      'option': 'alt'
      'command': 'meta'
      'return': 'enter'
      'escape': 'esc'
      'mod': if /Mac|iPod|iPhone|iPad/.test(navigator.platform) then 'meta'  else 'ctrl'
    }

    _KEYS = {
      'meta': {metaKey: true}
      'shift': {shiftKey: true}
      'ctrl': {ctrlKey: true}
      'alt': {altKey: true}
    }

    # ['metaKey', 'shiftKey'...]
    _MODIFIERS = _.reduce(_.values(_KEYS), ((memo, key) -> memo.concat(_.keys(key))), [])

    _MAP = {
      8: 'backspace'
      9: 'tab'
      13: 'enter'
      16: 'shift'
      17: 'ctrl'
      18: 'alt'
      20: 'capslock'
      27: 'esc'
      32: 'space'
      33: 'pageup'
      34: 'pagedown'
      35: 'end'
      36: 'home'
      37: 'left'
      38: 'up'
      39: 'right'
      40: 'down'
      45: 'ins'
      46: 'del'
      91: 'meta'
      93: 'meta'
      224: 'meta'
    }

    # loop through the f keys, f1 to f19 and add them to the map programatically
    _MAP[111 + i] = 'f' + i for i in [1..19]

    # loop through to map numbers on the numeric keypad
    _MAP[i + 96] = i for i in [0..9]

    combosArray = [] # array of combos defined on this element

    keys = scope.$eval(attrs.arkKeyBroadcast)
    for combo, broadcast of keys
      combo = _.reduce(combo.split('+'), ((memo, key) ->
        key = _SPECIAL_ALIASES[key] || key
        _.extend(memo, _KEYS[key] || {which: key})
      ), {})
      for modifier in _MODIFIERS
        combo[modifier] = false unless combo[modifier] == true
      combosArray.push({keys: combo, broadcast: broadcast})

    handleEvent = (event) ->
      eventKeys = _.pick(event, _MODIFIERS, 'which') # choose only the things we are interested in from event
      char = String.fromCharCode(event.which)
      if char && event.type == 'keypress'
        char = char.toLowerCase() unless eventKeys.shiftKey
        eventKeys.which = char
      else
        # turn .which == 13 into .which == 'enter'
        eventKeys.which = _MAP[eventKeys.which] || char.toLowerCase() || event.which
      for combo in combosArray
        if _.isEqual(combo.keys, eventKeys)
          $rootScope.$broadcast(combo.broadcast)
          return

    element.bind('keydown keypress', handleEvent)
)
