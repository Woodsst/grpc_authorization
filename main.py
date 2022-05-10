from server.server import server_run
from server.logger_config import logger_config
import logging

logger = logging.getLogger()


if __name__ == '__main__':
    logger_config()
    logger.info("i'm born")
    server_run()

