cached = require 'gulp-cached'
coffee = require 'gulp-coffee'
concat = require 'gulp-concat'
gcson = require 'gulp-cson'
gulp = require 'gulp'
ngAnnotate = require 'gulp-ng-annotate'
slim = require 'gulp-slim'
sourcemaps = require 'gulp-sourcemaps'

bowerJavaScript = [
  'jquery/dist/jquery.js'
  'bootstrap/dist/js/bootstrap.js'
  'angular/angular.js'
  'angular-resource/angular-resource.js'
  'ui-router/release/angular-ui-router.js'
]

swallowError = (err) ->
  console.log(err.toString())
  @emit 'end'

gulp.task 'bower:js', ->
  gulp.src(("bower_components/#{fname}" for fname in bowerJavaScript))
    .pipe(concat('vendor.js').on('error', swallowError))
    .pipe(gulp.dest('static/js'))

# If you uglify this you need to make it angular dependency injection aware
gulp.task 'coffee', ->
  gulp.src(('js/**/*.coffee'))
    .pipe(sourcemaps.init())
    .pipe(coffee().on('error', swallowError))
    .pipe(ngAnnotate())
    .pipe(concat('app.js').on('error', swallowError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('static/js'))

gulp.task 'slim', ->
  gulp.src(('html/**/*.slim'))
    .pipe(cached('slim'))
    .pipe(slim(pretty: true))
    .pipe(gulp.dest('static/html'))

gulp.task 'cson', ->
  gulp.src('*.cson')
    .pipe(gcson())
    .pipe(gulp.dest('.'))

gulp.task 'build', ['coffee', 'slim', 'cson', 'bower:js']

gulp.task 'watch', ['build'], ->
  gulp.watch 'js/**/*.coffee', ['coffee']
  gulp.watch 'html/**/*.slim', ['slim']
  gulp.watch '*.cson', ['cson']
  gulp.watch 'bower_components/**/*.js', ['bower:js']

gulp.task 'default', ['watch']
