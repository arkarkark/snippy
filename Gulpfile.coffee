cached = require 'gulp-cached'
coffee = require 'gulp-coffee'
gcson = require 'gulp-cson'
gulp = require 'gulp'
slim = require 'gulp-slim'
sourcemaps = require 'gulp-sourcemaps'

swallowError = (err) ->
  console.log(err.toString())
  @emit 'end'

gulp.task 'coffee', ->
  gulp.src(("js/**/*.coffee"))
    .pipe(cached("coffee"))
    .pipe(sourcemaps.init())
    .pipe(coffee().on('error', swallowError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest("static/js"))

gulp.task 'slim', ->
  gulp.src(("html/**/*.slim"))
    .pipe(cached("slim"))
    .pipe(slim(pretty: true))
    .pipe(gulp.dest("static/html"))

gulp.task 'cson', ->
  gulp.src('*.cson')
    .pipe(gcson())
    .pipe(gulp.dest('.'))

gulp.task 'build', ['coffee', 'slim', 'cson']

gulp.task 'watch', ['build'], ->
  gulp.watch "src/**/*.coffee", ['coffee']
  gulp.watch "html/**/*.slim", ['slim']
  gulp.watch "*.cson", ['cson']

gulp.task 'default', ['watch']
