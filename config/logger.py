import sys
from loguru import logger

def filter_only_my_package(record):
    return record["name"].startswith("")

def init_logger():
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        filter=filter_only_my_package
    )
    logger.add(
        "logs/logs.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        mode="w",  # 'w' для перезаписи, 'a' для дополнения (по умолчанию)
        filter=filter_only_my_package,
        encoding="utf-8"
    )

init_logger()