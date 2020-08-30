import logging
import logging.config
from odds_portal_scraper.logs.settings import logger_config


logging.config.dictConfig(logger_config)
app_logger = logging.getLogger('app_logger')
