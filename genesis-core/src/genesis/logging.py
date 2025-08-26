import logging

def setup_logger(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("genesis")
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        ch = logging.StreamHandler()
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger
