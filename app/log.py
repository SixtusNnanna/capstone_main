import logging
from logging.handlers import SysLogHandler


PAPERTRAIL_HOST = "logs6.papertrailapp.com"
PAPERTRAIL_PORT = 20597

handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
        handler
    ]
)
def get_logger(name):
    logger = logging.getLogger(name)
    return logger



