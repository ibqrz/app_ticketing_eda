import logging
import threading
import time
from contextlib import contextmanager

from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from common.config import settings

logger = logging.getLogger(__name__)

_pool = None
_lock = threading.Lock()


def _open(attempts=30, delay=2):
    for attempt in range(1, attempts + 1):
        try:
            return ThreadedConnectionPool(1, 10, settings.database_url)
        except OperationalError:
            logger.warning("database unavailable, attempt %s/%s", attempt, attempts)
            time.sleep(delay)
    raise ConnectionError("database unavailable")


def pool():
    global _pool
    if _pool is None:
        with _lock:
            if _pool is None:
                _pool = _open()
    return _pool


@contextmanager
def transaction():
    connection = pool().getconn()
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        pool().putconn(connection)