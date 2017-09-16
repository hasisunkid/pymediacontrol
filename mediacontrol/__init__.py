from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from mediacontrol import shairportcontrol as spc


app = Flask(__name__)

Bootstrap(app)

app.config.from_object('mediacontrol.configuration.DevelopmentConfig')

log = app.logger

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = RotatingFileHandler('{0}/{1}.log'.format(app.config['LOG_PATH'],
                                              app.config['LOGGER_NAME']),
                         maxBytes=10000, backupCount=4)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

#run metadate reader
spc.runBackround(pipe='/tmp/shairport/metadata',basepath='/home/enrico/Development/python/pymediacontrol/mediacontrol/static')

from mediacontrol import views
