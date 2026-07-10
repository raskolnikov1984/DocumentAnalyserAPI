import sys
from pathlib import Path

from loguru import logger


def configure_logging(environment: str = "development") -> None:
    logger.remove()

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    if environment == "production":
        logger.add(
            sys.stdout,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
                "{name}:{function}:{line} | {message}"
            ),
            level="INFO",
            serialize=True,
        )
        logger.add(
            log_dir / "cbam_{time:YYYY-MM-DD}.log",
            rotation="10 MB",
            retention="30 days",
            level="INFO",
            serialize=True,
        )
    else:
        logger.add(
            sys.stdout,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            level="DEBUG",
            colorize=True,
        )
        logger.add(
            log_dir / "cbam_{time:YYYY-MM-DD}.log",
            rotation="10 MB",
            retention="7 days",
            level="DEBUG",
        )

    logger.info(
        "Logging configured for {environment} environment", environment=environment
    )
