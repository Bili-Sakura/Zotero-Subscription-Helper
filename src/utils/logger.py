import logging
import os


class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()  # Ensure the log is flushed after each log entry


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        os.makedirs("logs", exist_ok=True)  # Ensure the logs directory exists
        handler = FlushFileHandler("logs/app.log", mode="a", encoding="utf-8")
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
