import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_credentials() -> tuple[str, str, str]:
    """Retrieve database credentials from environment variables and validate them."""
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD")

    if not db_password:
        raise ValueError(
            "❌ Database password is missing! Set DB_PASSWORD in the .env file or environment variables."
        )

    return db_host, db_user, db_password


def create_database(db_to_create: str = "star_schema_db") -> None:
    """Creates a database but does not return a connection."""
    try:
        db_host, db_user, db_password = get_db_credentials()
        conn = psycopg2.connect(
            host=db_host, dbname="postgres", user=db_user, password=db_password
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {db_to_create}")
        cur.execute(
            f"CREATE DATABASE {db_to_create} WITH ENCODING 'utf8' TEMPLATE template0"
        )

        cur.close()
        conn.close()
        print("✅ Database created successfully.")

    except ValueError as e:
        print(e)
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")


def connect_to_database(
    db_to_connect_to="star_schema_db",
) -> psycopg2.extensions.connection:
    """Connects to the database and returns a connection."""
    try:
        db_host, db_user, db_password = get_db_credentials()
        conn = psycopg2.connect(
            host=db_host, dbname=db_to_connect_to, user=db_user, password=db_password
        )
        print(f"✅ Connected to the {db_to_connect_to} database successfully.")
        return conn

    except ValueError as e:
        print(e)
    except psycopg2.Error as e:
        print(f"❌ Error connecting to {db_to_connect_to} database: {e}")
