autoprefixer = require 'gulp-autoprefixer'
cached = require 'gulp-cached'
coffee = require 'gulp-coffee'
concat = require 'gulp-concat'
gulp = require 'gulp'
ngAnnotate = require 'gulp-ng-annotate'
rename = require 'gulp-rename'
sass = require 'gulp-ruby-sass'
slim = require 'gulp-slim'
sourcemaps = require 'gulp-sourcemaps'
notify = require 'gulp-notify'

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
  'angular-bootstrap/ui-bootstrap-tpls.js'
  'angular-busy/dist/angular-busy.js'
]

bowerCss = [
  'bootstrap/dist/css/bootstrap.min.css'
  'angular-busy/dist/angular-busy.css'
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
  gulp.src(('app/**/*.slim'))
    .pipe(cached('slim'))
    .pipe(rename((path) ->
      path.dirname = path.dirname.replace(/^(html|js)(\/|$)/, '')
      path
    ))
    .pipe(slim(pretty: true))
    .pipe(gulp.dest('app/static/html'))

gulp.task 'icons', ->
  gulp.src('bower_components/fontawesome/fonts/**.*')
    .pipe(gulp.dest('./app/static/fonts'))

gulp.task 'css', ->
  sass('app/css/snip.scss', {
      loadPath: [
        'bower_components/fontawesome/scss'
      ]
    }).on('error', swallowError)
    .pipe(sourcemaps.write())
    .pipe(gulp.dest("app/static/css"))

gulp.task 'build', ['coffee', 'slim', 'bower:js', 'bower:css']

gulp.task 'watch', ['build'], ->
  gulp.watch 'app/js/**/*.coffee', ['coffee']
  gulp.watch 'app/**/*.slim', ['slim']
  gulp.watch 'app/css/**/*.scss', ['css']

gulp.task 'default', ['watch']
