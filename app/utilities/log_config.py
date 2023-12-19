# import logging

# class CustomFormatter(logging.Formatter):

#     grey = "\x1b[38;20m"
#     yellow = "\x1b[33;20m"
#     red = "\x1b[31;20m"
#     bold_red = "\x1b[31;1m"
#     reset = "\x1b[0m"
#     format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

#     FORMATS = {
#         logging.DEBUG: grey + format + reset,
#         logging.INFO: grey + format + reset,
#         logging.WARNING: yellow + format + reset,
#         logging.ERROR: red + format + reset,
#         logging.CRITICAL: bold_red + format + reset
#     }

#     def format(self, record):
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)
    
# class AppLogger():
#     def __init__(self, log_level=logging.DEBUG):

#         grey = "\x1b[38;20m"
#         yellow = "\x1b[33;20m"
#         red = "\x1b[31;20m"
#         bold_red = "\x1b[31;1m"
#         reset = "\x1b[0m"
#         format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

#         FORMATS = {
#             logging.DEBUG: grey + format + reset,
#             logging.INFO: grey + format + reset,
#             logging.WARNING: yellow + format + reset,
#             logging.ERROR: red + format + reset,
#             logging.CRITICAL: bold_red + format + reset
#         }

#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(log_level)

#         # Create a file handler and set the log level
#         # file_handler = logging.FileHandler(log_file)
#         file_handler.setLevel(log_level)

#         # Create a formatter and set the format for log entries
#         formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#         file_handler.setFormatter(formatter)

#         # Add the file handler to the logger
#         self.logger.addHandler(file_handler)

#     def log_info(self, message):
#         self.logger.info(message)

#     def log_warning(self, message):
#         self.logger.warning(message)

#     def log_error(self, message):
#         self.logger.error(message)

#     def log_debug(self, message):
#         self.logger.debug(message)