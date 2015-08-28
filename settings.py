APP_HOST = '0.0.0.0'
APP_PORT = '8000'

#"DEBUG", "INFO","WARNING", "ERROR", "CRITICAL"
DEBUG = False
LOG_INFO = True

SECRET_KEY = 'Good man is well done'

MONGODB_DATABASE = "mongodb://localhost:27017"


#SQLALCHEMY_DATABASE_URI = 'mysql://root@33.33.33.10:3306/overholt'
CELERY_BROKER_URL = 'redis://33.33.33.10:6379/0'

USERNAME = 'admin'
PASSWORD = 'default'

REDIS_NAME = 'myredis'


LOG_FILE = "zuohaoshi.log"
