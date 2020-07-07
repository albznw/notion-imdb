import logging
import sys

# =============================== Set up logger ===============================#

logger = logging.getLogger("notion_imdb")
logger.setLevel(logging.DEBUG)

# Give logger the possibility to write to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - (%(threadName)-10s) - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# File handler
# handler = logging.FileHandler("counter.log", mode="w")
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter(
#     '%(asctime)s - (%(threadName)-10s) - %(levelname)s - %(message)s'
# )
# handler.setFormatter(formatter)
# logger.addHandler(handler)