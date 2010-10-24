#!/bin/sh
# start google appengine for python

# set python 2.5 as interpreter:
python2.5 $GOOGLE_APP_ENGINE/dev_appserver.py --address=0.0.0.0 --port=9999 ~/workspace/python/express-me/src
