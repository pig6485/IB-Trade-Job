import logging
import os
import logging.handlers

def setup_logging(log_file_path="app.log", level=logging.INFO):
    """`
    Configure the application's logging system.
    Logs will be output to both the console and a file.

    Args:
        log_file_path (str): The path to the log file.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
    """

    # Ensure the log file directory exists
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid adding duplicate handlers
    if not root_logger.handlers:
        # 1. Create a formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

        # 2. Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # 3. Create a file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a pre-configured Logger instance.

    Args:
        name: Logger name, usually __name__.

    Returns:
        Pre-configured Logger instance.
    """
    return logging.getLogger(name)