from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from contextlib import contextmanager

from config import db_config


pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=db_config.db_name,
    user=db_config.db_user,
    password=db_config.db_password,
    host=db_config.db_host,
    port=db_config.db_port,
)


@contextmanager
def get_cursor():
    """Provides a database cursor from the connection pool.

    Obtains a connection from the PostgreSQL connection pool, creates a
    cursor using ``RealDictCursor``, and yields it to the caller. If the
    operation completes successfully, the transaction is committed. If an
    exception occurs, the transaction is rolled back. In all cases, the
    connection is returned to the pool.

    Yields:
        cursor: PostgreSQL cursor configured with ``RealDictCursor``.
    """
    conn = pool.getconn()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        pool.putconn(conn)
