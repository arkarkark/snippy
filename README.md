# snippy

Snippy is a google app engine app for creating and serving your own short urls
it also has some other features:

* create short urls
* redirect while hiding the referer
* short urls protected by a login
* image proxy
* short urls also support suggestions

# Install

```bash
make setup
# run the dev server
make dev
# then make deploy
```

# More

Blog posts about it are here:

* [first version in php](http://blog.wtwf.com/2006/08/snippy-urls.php)
* [now in app engine](http://blog.wtwf.com/2010/04/snippy-urls-in-app-engine.html)
* [with suggest passthrough](http://blog.wtwf.com/2010/05/adding-suggest-passthrough-to-snippy.html)

Here's some short urls I use all the time

* w - make a new short url
* ws - search for short urls - to edit them
* g - google search
* gis - google image search
* qr - make a qr code for a url
* map - google maps
* go - google I'm feeling lucky
* yt - youtube search
* f - froogle search
* urban - urban dictionary search

Alternatives can be found here:

* [Tekno Bites: 10 Free Scripts to Create Your Own Url Shortening Service](http://www.teknobites.com/2009/04/16/10-free-scripts-to-create-your-own-url-shortening-service/)

# SSL Support!

You can get SSL support using letsencrypt with the following steps:

# Setup

Replace `example.com` with your domain, obvs.!

**NOTE**: the 2048 key length is really important app engine can't handle the 4096 that is in the `sign_csr.py` examples.

```
DOMAIN=example.com
openssl genrsa 2048 > user.key
openssl rsa -in user.key -pubout > user.pub
openssl genrsa 2048 > ${DOMAIN}.key
openssl req -new -sha256 -key ${DOMAIN}.key -subj "/" -reqexts SAN \
  -config <(cat /etc/ssl/openssl.cnf /System/Library/OpenSSL/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:${DOMAIN},DNS:www.${DOMAIN},DNS:app.${DOMAIN}")) \
  > ${DOMAIN}.csr

echo "Now go to http://${DOMAIN}/.well-known/acme-challenge/ and save that in acme-password.txt"
```

# Request certs (every 3 months)

```
DOMAIN=example.com
python letsencrypt-nosudo/sign_csr.py \
  --email letsencrypt@mail.example.com \
	--run-commands \
	--password-file="acme-password.txt" \
	--url-based \
  --public-key user.pub ${DOMAIN}.csr > ${DOMAIN}.signed.crt

echo "Go to https://console.cloud.google.com/appengine/settings/certificates to upload your new certs."
```

You'll need [MY letsencrypt-nosudo](https://github.com/arkarkark/letsencrypt-nosudo) for the --password-file and --run-commands and --url-based flags

## background reading

* [letsencrypt/letsencrypt#1480](https://github.com/letsencrypt/letsencrypt/issues/1480)
* [letsencrypt-nosudo](https://github.com/diafygi/letsencrypt-nosudo)
* [MY letsencrypt-nosudo](https://github.com/arkarkark/letsencrypt-nosudo)
* [well_known.py Handler](blob/master/app/well_known.py)
