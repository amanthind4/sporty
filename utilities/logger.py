import logging
import os



class LogGen:
    _logger = None

    @staticmethod
    def loggen():
        if LogGen._logger is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            log_dir = os.path.join(parent_dir, 'logs')
            try:
                os.makedirs(log_dir, exist_ok=True)
            except OSError as e:
                print(f"Error creating logs directory: {e}")
                raise
            log_file_path = os.path.join(log_dir, 'automation.log')

            LOG_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)-8s [%(name)-15s]: %(message)s'
            LOG_DATE_FORMAT = '%B %d, %Y %I:%M:%S %p'
            formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
            LogGen._logger = logging.getLogger(__name__)
            LogGen._logger.setLevel(logging.DEBUG)

            file_handler = logging.FileHandler(
                filename=log_file_path,
                mode='w'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            LogGen._logger.addHandler(file_handler)
            LogGen._logger.addHandler(console_handler)

        return LogGen._logger