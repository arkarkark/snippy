cached = require "gulp-cached"
coffee = require "gulp-coffee"
concat = require "gulp-concat"
eventStream = require "event-stream"
fs = require "fs"
gcson = require "gulp-cson"
glob = require "glob"
gulp = require "gulp"
gutil = require "gulp-util"
ignore = require "gulp-ignore"
ngAnnotate = require "gulp-ng-annotate"
rename = require "gulp-rename"
run = require "gulp-run"
sass = require "gulp-sass"
slm = require "gulp-slm"
sourcemaps = require "gulp-sourcemaps"
yargs = require "yargs"

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
  brandingDir ?= fs.readlinkSync("branding")
try
  brandingDir ?= fs.readFileSync("branding").toString()
brandingDir ?= "branding.wtwf"

nodeJavaScript = [
  "underscore/underscore.js"
  "jquery/dist/jquery.js"
  "bootstrap/dist/js/bootstrap.js"
  "angular/angular.js"
  "angular-resource/angular-resource.js"
  "ui-router/release/angular-ui-router.js"
  "qrcode-generator/js/qrcode.js"
  "angular-qrcode/angular-qrcode.js"
  "angular-ui-grid/ui-grid.js"
  "angular-bootstrap/ui-bootstrap-tpls.js"
  "angular-busy2/dist/angular-busy.js"
]

nodeCss = [
  "angular-busy/dist/angular-busy.css"
  "bootstrap/dist/css/bootstrap.css"
  "bootstrap/dist/css/bootstrap-theme.css"
]

swallowError = (err) ->
  console.log(err.toString())
  @emit "end"

# from http://stackoverflow.com/questions/23230569/how-do-you-create-a-file-from-a-string-in-gulp
srcFromString = (filename, string) ->
  src = require("stream").Readable(objectMode: true)
  src._read = ->
    this.push(new gutil.File(cwd: "", base: "", path: filename, contents: new Buffer(string)))
    this.push(null)
  src

gulp.task "node:js", ->
  gulp.src(("node_modules/#{fname}" for fname in nodeJavaScript))
    .pipe(concat("vendor.js").on("error", swallowError))
    .pipe(gulp.dest("app/static"))

# If you uglify this you need to make it angular dependency injection aware
gulp.task "coffee", ->
  gulp.src([
    "client/app.coffee"
    "client/*_module.coffee"
    "client/**/*.coffee"
    ])
    .pipe(sourcemaps.init())
    .pipe(coffee().on("error", swallowError))
    .pipe(ngAnnotate())
    .pipe(concat("app.js").on("error", swallowError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest("app/static"))

gulp.task "slim", ->
  gulp.src(("client/**/*.slim"))
    .pipe(cached("slim"))
    .pipe(slm({})).on("error", swallowError)
    .pipe(gulp.dest("app/static"))

gulp.task "icons", ->
  gulp.src("node_modules/font-awesome/fonts/**.*")
    .pipe(gulp.dest("./app/static"))

gulp.task "css", ->
  nodeFiles = gulp.src(("node_modules/#{fname}" for fname in nodeCss))

  vendorSass = """
    $fa-font-path: ".";
    @import "node_modules/font-awesome/scss/font-awesome";
  """
  clientSass = glob.sync("client/**/*.scss").map((fileName) ->
    """@import "#{fileName[0..-6]}";""").join("\n")

  sassFiles = srcFromString("snip.scss", vendorSass + clientSass)
    .pipe(sass()).on("error", swallowError)
    .pipe(sourcemaps.write())

  eventStream.concat(nodeFiles, sassFiles)
      .pipe(concat("snip.css"))
      .pipe(gulp.dest("app/static"))

gulp.task "brand", ->
  gulp.src("#{brandingDir}/static/**")
    .pipe(ignore.exclude("**.coffee"))
    .pipe(gulp.dest("./app/static"))
  gulp.src("#{brandingDir}/default.html")
    .pipe(gulp.dest("./app/brand"))
  gulp.src("#{brandingDir}/snippy_config.cson")
    .pipe(gcson())
    .pipe(gulp.dest("./app/brand"))

gulp.task "appyaml", ["brand"], ->
  run("./app/make_app.yaml.py").exec()

gulp.task "build", ["coffee", "slim", "node:js", "css", "icons", "brand", "appyaml"]

gulp.task "watch", ->
  gulp.watch "client/**/*.coffee", ["coffee"]
  gulp.watch "client/**/*.slim", ["slim"]
  gulp.watch "client/**/*.scss", ["css"]
  gulp.watch brandingDir + "/**/*", ["brand", "appyaml"]

gulp.task "dev", ["build", "watch"]

gulp.task "default", ["dev"]
