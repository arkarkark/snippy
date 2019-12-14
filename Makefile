dev:
	./node_modules/.bin/gulp & (cd app; dev_appserver.py --host=0.0.0.0 \
	  --port 6723 \
	  --admin_port 6724 \
	.)

setup: vendor app/jsonpath_rw app/dateutil app/bouncer app/well_known.py
	yarn

clean:
	cd app; rm -f -v bouncer dateutil decorator.py jsonpath* ply six.py well_known.py
	rm -rf vendor

deploy: setup
	./node_modules/.bin/gulp build
	(cd app; gcloud --quiet app --project wtwfappy deploy --version=13)

test:
	for fil in app/*_test.py; do $$fil; done

################################################################

vendor:
	mkdir -p vendor

vendor/six:
	git -C vendor clone git@github.com:benjaminp/six.git

app/six.py: vendor/six
	cd app; ln -s -f ../vendor/six/six.py

vendor/decorator:
	git -C vendor clone git@github.com:micheles/decorator.git

app/decorator.py: vendor/decorator
	cd app; ln -s -f ../vendor/decorator/src/decorator.py

vendor/ply-3.11:
	curl -o - http://www.dabeaz.com/ply/ply-3.11.tar.gz | tar -zxv -C vendor -f -

app/ply: vendor/ply-3.11
	cd app; ln -s -f ../vendor/ply-3.11/ply

vendor/jsonpath_rw:
	git -C vendor clone git@github.com:kennknowles/python-jsonpath-rw.git jsonpath_rw

app/jsonpath_rw: app/ply app/decorator.py app/six.py vendor/jsonpath_rw
	cd app; ln -s -f ../vendor/jsonpath_rw/jsonpath_rw

vendor/python-dateutil-1.5:
	curl -o - http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz | \
	  tar -zxv -C vendor -f -

app/dateutil: vendor/python-dateutil-1.5
	cd app; ln -s -f ../vendor/python-dateutil-1.5/dateutil dateutil

vendor/bouncer:
	git -C vendor clone git@github.com:bouncer-app/bouncer.git

app/bouncer: vendor/bouncer
	cd app; ln -s -f ../vendor/bouncer/bouncer bouncer

app/well_known.py: vendor/letsencrypt-nosudo
	cd app; ln -s -f ../vendor/letsencrypt-nosudo/contrib/appengine/well_known.py

vendor/letsencrypt-nosudo:
	git -C vendor clone git@github.com:arkarkark/letsencrypt-nosudo.git
