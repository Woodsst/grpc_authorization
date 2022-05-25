from server.server import server_run
from server.config import Settings
from server.orm import Orm
from server.logger_config import logger_config
import logging

logger = logging.getLogger()


if __name__ == '__main__':
    logger_config()
    config = Settings()
    orm = Orm(config)
    logger.info("i'm born")
    server_run(orm)
