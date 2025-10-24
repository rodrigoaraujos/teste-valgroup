import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)
logger.add(
    "logs/app.log",  # caminho do arquivo
    rotation="10 MB",  # cria novo arquivo a cada 10 MB
    retention="10 days",  # mantém logs por 10 dias
    compression="zip",  # comprime logs antigos
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
)
