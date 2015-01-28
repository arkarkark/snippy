dev:
	./node_modules/gulp/bin/gulp.js &
	(cd app; dev_appserver.py --host=0.0.0.0 .)

setup:
	bundle install
	npm install
	bower install
	mkdir vendor
	curl -o - http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz | \
		tar -zxv -C vendor -f -
	(cd app; ln -s ../vendor/python-dateutil-1.5/dateutil dateutil)

install:
	./node_modules/gulp/bin/gulp.js build
	(cd app; appcfg.py --oauth2 update .)
