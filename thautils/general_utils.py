import logging


def create_logger(logger_name: str = None,
                  logfile: str = None,
                  level: str = "INFO",
                  file_level: str = None) -> logging.Logger:
    ### ref: https://realpython.com/python-logging/#using-handlers
    """ Create a logger"""
    # c_: means console; f_: means file

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    c_level = level_map.get(level)
    f_level = level_map.get(file_level) if file_level else c_level
    logger_name = logger_name if logger_name else __name__

    # Create a custom logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(c_level)  # to show log in jupyter notebook

    # Create handlers
    c_handler = logging.StreamHandler()
    c_handler.setLevel(c_level)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(levelname)s - %(message)s | %(name)s - %(funcName)s:%(lineno)d')
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    ### Add a file handler
    if logfile:
        f_handler = logging.FileHandler(logfile)
        f_handler.setLevel(f_level)
        f_format = logging.Formatter('%(asctime)s | %(levelname)s - %(message)s | %(name)s')
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger
