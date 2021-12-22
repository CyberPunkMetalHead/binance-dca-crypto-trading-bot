import logging
FORMAT = '%(levelname)s: %(asctime)s | FILE: %(filename)s:%(lineno)d | MESSAGE: %(message)s'
logging.basicConfig(filename = 'log.log', level=logging.INFO, format = FORMAT )
logger = logging.getLogger(__name__)
