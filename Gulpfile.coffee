cached = require 'gulp-cached'
coffee = require 'gulp-coffee'
concat = require 'gulp-concat'
gcson = require 'gulp-cson'
gulp = require 'gulp'
ngAnnotate = require 'gulp-ng-annotate'
slim = require 'gulp-slim'
sourcemaps = require 'gulp-sourcemaps'

bowerJavaScript = [
  'underscore/underscore.js'
  'jquery/dist/jquery.js'
  'bootstrap/dist/js/bootstrap.js'
  'angular/angular.js'
  'angular-resource/angular-resource.js'
  'ui-router/release/angular-ui-router.js'
  'qrcode-generator/js/qrcode.js'
  'angular-qrcode/qrcode.js'
  'angular-ui-grid/ui-grid.js'
  'angular-bootstrap/ui-bootstrap.js'
]

bowerCss = [
  'bootstrap/dist/css/bootstrap.min.css'
]

swallowError = (err) ->
  console.log(err.toString())
  @emit 'end'

gulp.task 'bower:js', ->
  gulp.src(("bower_components/#{fname}" for fname in bowerJavaScript))
    .pipe(concat('vendor.js').on('error', swallowError))
    .pipe(gulp.dest('app/static/js'))

gulp.task 'bower:css', ->
  gulp.src(("bower_components/#{fname}" for fname in bowerCss))
    .pipe(concat('vendor.css').on('error', swallowError))
    .pipe(gulp.dest('app/static/css'))

# If you uglify this you need to make it angular dependency injection aware
gulp.task 'coffee', ->
  gulp.src(('app/js/**/*.coffee'))
    .pipe(sourcemaps.init())
    .pipe(coffee().on('error', swallowError))
    .pipe(ngAnnotate())
    .pipe(concat('app.js').on('error', swallowError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('app/static/js'))

gulp.task 'slim', ->
  gulp.src(('app/html/**/*.slim'))
    .pipe(cached('slim'))
    .pipe(slim(pretty: true))
    .pipe(gulp.dest('app/static/html'))

gulp.task 'cson', ->
  gulp.src('./*.cson')
    .pipe(gcson())
    .pipe(gulp.dest('.'))

gulp.task 'build', ['coffee', 'slim', 'cson', 'bower:js', 'bower:css']

gulp.task 'watch', ['build'], ->
  gulp.watch 'app/js/**/*.coffee', ['coffee']
  gulp.watch 'app/html/**/*.slim', ['slim']
  gulp.watch './*.cson', ['cson']

gulp.task 'default', ['watch']
