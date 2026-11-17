import logging

from common.config import settings


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=f"%(asctime)s [{settings.instance_id}] %(levelname)s %(message)s",
    )
    logging.getLogger("pika").setLevel(logging.WARNING)
