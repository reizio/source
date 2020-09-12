import logging

logger = logging.getLogger("source")
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(funcName)-15s --- %(message)s",
    datefmt="%m-%d %H:%M",
)
