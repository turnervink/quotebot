import psycopg2
import psycopg2.extras

PAGE_SIZE = 10


class Postgres:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            cursor_factory=psycopg2.extras.DictCursor
        )

    def get_all_quotes(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM quote ORDER BY created_at DESC")
                return cur.fetchall()

    def get_random_quote(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM quote ORDER BY RANDOM() LIMIT 1")
                return cur.fetchone()

    def search_quotes(self, search_term=None, author=None, page=1):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM quote
                        WHERE
                            (%s IS NULL OR quote ILIKE %s) AND
                            (%s IS NULL OR author ILIKE %s)
                    ORDER BY created_at DESC
                    LIMIT %s
                    OFFSET %s
                    """,
                    (search_term, f"%{search_term}%", author,
                     author, PAGE_SIZE, (page - 1) * PAGE_SIZE)
                )
                return cur.fetchall()

    def get_total_search_matches(self, search_term=None, author=None):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM quote
                    WHERE
                        (%s IS NULL OR quote ILIKE %s) AND
                        (%s IS NULL OR author ILIKE %s)
                    """,
                    (search_term, f"%{search_term}%", author, author)
                )
                return cur.fetchone()[0]

    def add_quote(self, quote, author, freeform_date):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO quote (quote, author, freeform_date)
                    VALUES (%s, %s, %s)
                    """,
                    (quote, author, freeform_date)
                )
