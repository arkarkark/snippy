local:
	dev_appserver.py .

install:
	appcfg.py --oauth2 update .
