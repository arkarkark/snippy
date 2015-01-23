angular.module('QrCode', []).factory('QrService', ->
  qrLookup = [ # from https://developers.google.com/chart/infographics/docs/qr_codes
    {version: 1, level: 'H', digits: 17, chars: 10, binary: 7, kanji: 4},
    {version: 1, level: 'Q', digits: 27, chars: 16, binary: 11, kanji: 7},
    {version: 1, level: 'M', digits: 34, chars: 20, binary: 14, kanji: 8},
    {version: 1, level: 'L', digits: 41, chars: 25, binary: 17, kanji: 10},
    {version: 2, level: 'H', digits: 34, chars: 20, binary: 14, kanji: 8},
    {version: 2, level: 'Q', digits: 48, chars: 29, binary: 20, kanji: 12},
    {version: 2, level: 'M', digits: 63, chars: 38, binary: 26, kanji: 16},
    {version: 2, level: 'L', digits: 77, chars: 47, binary: 32, kanji: 20},
    {version: 3, level: 'H', digits: 58, chars: 35, binary: 24, kanji: 15},
    {version: 3, level: 'Q', digits: 77, chars: 47, binary: 32, kanji: 20},
    {version: 3, level: 'M', digits: 101, chars: 61, binary: 42, kanji: 26},
    {version: 3, level: 'L', digits: 127, chars: 77, binary: 53, kanji: 32},
    {version: 4, level: 'H', digits: 82, chars: 50, binary: 34, kanji: 21},
    {version: 4, level: 'Q', digits: 111, chars: 67, binary: 46, kanji: 28},
    {version: 4, level: 'M', digits: 149, chars: 90, binary: 62, kanji: 38},
    {version: 4, level: 'L', digits: 187, chars: 114, binary: 78, kanji: 48}
  ]

  @settings = (data) =>
    length = data.length
    _.find(qrLookup, (q) -> q.binary  > length)

  @
)
