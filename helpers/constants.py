# Database constants
SQLALCHEMY_DATABASE_URL = "postgresql:///steven" #CHANGEME
NUMBER_OF_ITEMS_FOR_DATABASE = 100

# Webserver constants
WEBSERVER_ADDRESS = "127.0.0.1"
WEB_SERVER_HOST = f"http://{WEBSERVER_ADDRESS}"
DEFAULT_PORT = "5000"
WAIT_PORT = "5001"
WEB_SERVER_HOST_WITH_PORT = f"{WEB_SERVER_HOST}:{DEFAULT_PORT}"
WAIT_URL = f"{WEB_SERVER_HOST}:{WAIT_PORT}/wait"
DEFAULT_WORKERS = "4"

# Misc constants
WRK_PATH = "/home/steven/wrk/wrk" #CHANGEME