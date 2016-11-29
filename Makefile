dev:
	./node_modules/.bin/gulp & (cd app; dev_appserver.py --host=0.0.0.0 \
	  --port 6723 \
	  --admin_port 6724 \
	.)

setup:
	npm install
	mkdir -p vendor
	if [ ! -d vendor/python-dateutil-1.5 ]; then \
	  curl -o - http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz | \
		tar -zxv -C vendor -f -; \
	fi
	(cd app; ln -s -f ../vendor/python-dateutil-1.5/dateutil dateutil)
	if [ ! -d vendor/bouncer ]; then (git -C vendor clone git@github.com:bouncer-app/bouncer.git); fi
	(cd app; ln -s -f ../vendor/bouncer/bouncer bouncer)
	if [ ! -e app/well_known.py ]; then \
	  if [ ! -e vendor/letsencrypt-nosudo ]; then \
	    git -C vendor clone git@github.com:arkarkark/letsencrypt-nosudo.git; \
	  fi; \
	  (cd app; ln -s -f ../vendor/letsencrypt-nosudo/contrib/appengine/well_known.py); \
	fi


deploy: setup
	./node_modules/.bin/gulp build
	(cd app; gcloud --quiet app --project wtwfappy deploy --version=10)

test:
	for fil in app/*_test.py; do $$fil; done
