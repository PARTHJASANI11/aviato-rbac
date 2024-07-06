import logging

class Logger:
    """
    Class to define logger 
    """
    logger_instance = None

    def __init__(self, name: str, log_level: str = "INFO") -> None:
        """
        Set name and log level in the logger  

        :param name: Name of the logger
        :param log_level: Level of the log
        """
        self.name = name
        self.log_level = log_level

    @property
    def logger(self) -> logging.Logger:
        """
        Method to return logger instance 
        """
        if not Logger.logger_instance:
            Logger.logger_instance = self.get_logger_instance()
        return Logger.logger_instance

    def get_logger_instance(self) -> logging.Logger:
        """
        To get the logger instance
        
        :returns Logger: Logger object
        """
        logger = logging.getLogger(self.name)
        logger.propagate = False
        logger.setLevel(self.log_level)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(funcName)s | %(message)s")

        gunicorn_logger = logging.getLogger("gunicorn.error")
        gunicorn_logger.propagate = False
        gunicorn_logger.setLevel(self.log_level)

        for handler in gunicorn_logger.handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger


logger = Logger("aviato-rbac").logger
