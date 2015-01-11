dev:
	dev_appserver.py --host=0.0.0.0 .

install:
	appcfg.py --oauth2 update .
