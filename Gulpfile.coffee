autoprefixer = require 'gulp-autoprefixer'
cached = require 'gulp-cached'
coffee = require 'gulp-coffee'
concat = require 'gulp-concat'
eventStream = require 'event-stream'
fs = require 'fs'
gcson = require 'gulp-cson'
gulp = require 'gulp'
ngAnnotate = require 'gulp-ng-annotate'
rename = require 'gulp-rename'
run = require 'gulp-run'
sass = require 'gulp-ruby-sass'
slim = require 'gulp-slim'
sourcemaps = require 'gulp-sourcemaps'
notify = require 'gulp-notify'
yargs = require 'yargs'

argv = yargs.argv

# You can now choose the branding of snippy
# copy snippy_config.json, favicon.ico and default.html from branding.wtwf into branding.yourdomain
# You can specify the branding directory to use several ways.
# gulp --branding=branding.yourdomain
# or ONE of these...
# echo branding.yourdomain > branding
# ln -s branding.yourdomain branding
brandingDir = argv.branding
try
  brandingDir ?= fs.readlinkSync('branding')
try
  brandingDir ?= fs.readFileSync('branding').toString()
brandingDir ?= 'branding.wtwf'

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
  'URL.js/dist/URL.js'
]

bowerCss = [
  'angular-busy/dist/angular-busy.css'
]

swallowError = (err) ->
  console.log(err.toString())
  @emit 'end'

gulp.task 'bower:js', ->
  gulp.src(("bower_components/#{fname}" for fname in bowerJavaScript))
    .pipe(concat('vendor.js').on('error', swallowError))
    .pipe(gulp.dest('app/static/js'))

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
  bowerFiles = gulp.src(("bower_components/#{fname}" for fname in bowerCss))

  sassFiles = sass('app/css/snip.scss', {
      loadPath: [
        'bower_components/bootstrap-sass-official/assets/stylesheets'
        'bower_components/fontawesome/scss'
      ]
    }).on('error', swallowError)
    .pipe(sourcemaps.write())

  eventStream.concat(bowerFiles, sassFiles)
      .pipe(concat('snip.css'))
      .pipe(gulp.dest("app/static/css"))

gulp.task 'brand', ->
  gulp.src("#{brandingDir}/static/**")
    .pipe(gulp.dest('./app/static'))
  gulp.src("#{brandingDir}/default.html")
    .pipe(gulp.dest('./app/brand'))
  gulp.src("#{brandingDir}/snippy_config.cson")
    .pipe(gcson())
    .pipe(gulp.dest('./app/brand'))

gulp.task 'appyaml', ['brand'], ->
  run('./app/make_app.yaml.py').exec()

gulp.task 'build', ['coffee', 'slim', 'bower:js', 'css', 'icons', 'brand', 'appyaml']

gulp.task 'watch', ->
  gulp.watch 'app/js/**/*.coffee', ['coffee']
  gulp.watch 'app/**/*.slim', ['slim']
  gulp.watch 'app/css/**/*.scss', ['css']
  gulp.watch brandingDir + '/**/*', ['brand', 'appyaml']

gulp.task 'dev', ['build', 'watch']

gulp.task 'default', ['dev']
