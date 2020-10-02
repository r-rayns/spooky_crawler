"""
article_accepted
"""

from yoyo import step

__depends__ = {'0000_initial_schema'}

steps = [
    step(
        """
        ALTER TABLE articles
        ADD accepted BOOLEAN DEFAULT FALSE
        """,
        """
        ALTER TABLE articles
        DROP COLUMN accepted
        """
    )
]
