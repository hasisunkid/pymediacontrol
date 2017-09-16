class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///application.db'
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "MINHACHAVESECRETA"
    CSRF_ENABLED = True
    LOGGER_NAME = "MediaControll"
    HOST_ADDRESS = "zbox"
    PORT = 8050 
    LOG_PATH = "log"
    # Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
    RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
    RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'xxx@xxx'
    MAIL_PASSWORD = 'xxxxx'


class DevelopmentConfig(Config):
    DEBUG = True


class Distributet(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/application.db'
    LOG_PATH = "log"


class TestingConfig(Config):
    TESTING = True

if __name__ == '__main__':
    c = Distributet()
    c.write("test.cfg")
