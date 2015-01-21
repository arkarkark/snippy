dev:
	./node_modules/gulp/bin/gulp.js &
	(cd app; dev_appserver.py --host=0.0.0.0 .)

install:
	./node_modules/gulp/bin/gulp.js build
	(cd app; appcfg.py --oauth2 update .)
