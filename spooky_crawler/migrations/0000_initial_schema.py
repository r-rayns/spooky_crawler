"""
initial_schema
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
        """,
        """
        DROP EXTENSION IF EXISTS "uuid-ossp"
        """
    ),
    step(
        "CREATE TABLE publishers (publisher_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY, name VARCHAR(255) NOT NULL, label VARCHAR(255) NOT NULL, lat_lng POINT NOT NULL)",
        "DROP TABLE publishers"
    ),
    step(
        "CREATE TYPE article_types AS ENUM('ghost', 'ufo', 'weird')",
        "DROP TYPE article_types"
    ),
    step(
        """
        CREATE TABLE articles (
            article_id uuid DEFAULT uuid_generate_v4 () PRIMARY KEY,
            publisher_id uuid NOT NULL,
            publisher VARCHAR(255) NOT NULL,
            date_published timestamp without time zone NOT NULL,
            date_retrieved timestamp without time zone NOT NULL DEFAULT CURRENT_DATE,
            title VARCHAR(255) NOT NULL UNIQUE,
            description VARCHAR(500),
            link VARCHAR(2000) NOT NULL,
            article_type article_types,
            FOREIGN KEY (publisher_id)
            REFERENCES publishers (publisher_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        "DROP TABLE articles"
    ),
    step(
        "INSERT INTO publishers (name, label, lat_lng) VALUES ('liverpoolecho', 'Liverpool Echo', '53.408371,-2.991573')",
        "DELETE FROM publishers WHERE name IN ('liverpoolecho')"
    )
]
