import logging

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(threadName)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    #logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s", filename="sensaweb.log")
    return logger
