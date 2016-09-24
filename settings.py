# app
APP_HOST = '0.0.0.0'
APP_PORT = '8000'

# "DEBUG", "INFO","WARNING", "ERROR", "CRITICAL"
DEBUG = False
LOG_INFO = True
LOG_FILE = "/var/log/zuohaoshi/zuohaoshi.log"

UPLOAD_FOLDER = "/var/log/zuohaoshi"

SECRET_KEY = 'goodman'

# MONGODB_DATABASE = "mongodb://localhost:27017"
MONGODB_DATABASE = "mongodb://172.17.42.1:27017"

# SQLALCHEMY_DATABASE_URI = 'mysql://root@33.33.33.10:3306/overholt'

USERNAME = 'admin'
PASSWORD = 'default'

REDIS_DB_HOST = '127.0.0.1'
REDIS_DB_PORT = '6379'
REDIS_NAME = 'myredis'



