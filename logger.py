import logging


class Logger:
    def __init__(self, module_name: str):
        # create logger
        self._logger = logging.getLogger(module_name)
        self._logger.setLevel(logging.INFO)
        
        # create file handler
        file_handler = logging.FileHandler('core.log', mode='w')
        file_handler.setLevel(logging.INFO)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self._logger.addHandler(ch)
        self._logger.addHandler(file_handler)
        

    def debug(self, msg):
        self._logger.debug(msg)
        
    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)    