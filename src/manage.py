# coding=utf-8

from app import create_app

app = create_app()

app.run(host='0.0.0.0',port=8443)
#app.run(host='0.0.0.0', port=8443,
#       ssl_context=('/etc/letsencrypt/live/dero.cash/fullchain.pem', '/etc/letsencrypt/live/dero.cash/privkey.pem'))
