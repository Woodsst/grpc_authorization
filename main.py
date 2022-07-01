from server.server import server_run
from server.config import Settings
from server.orm import Orm
from server.logger_config import logger


if __name__ == '__main__':
    config = Settings()
    orm = Orm(config)
    logger.info("authorization server start")
    try:
        server_run(orm)
    except KeyboardInterrupt:
        pass
