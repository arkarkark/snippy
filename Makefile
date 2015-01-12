dev:
	./node_modules/gulp/bin/gulp.js &
	dev_appserver.py --host=0.0.0.0 .

install:
	./node_modules/gulp/bin/gulp.js build
	appcfg.py --oauth2 update .
