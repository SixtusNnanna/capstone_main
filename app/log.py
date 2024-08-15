import os 
import logging

from logging.handlers import SysLogHandler
from dotenv import load_dotenv





logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
  
    ]
)
def get_logger(name):
    logger = logging.getLogger(name)
    return logger



