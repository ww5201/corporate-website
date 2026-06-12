#!/bin/bash
base64 -d /tmp/html.b64 > /var/www/frontend/index.html
wc -c /var/www/frontend/index.html
nginx -s reload
echo DONE