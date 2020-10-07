"""
increase title length
"""

from yoyo import step

__depends__ = {'0001_article_accepted'}

steps = [
    step(
        """
        ALTER TABLE articles
        ALTER COLUMN title TYPE VARCHAR(2000)
        """,
        """
        ALTER TABLE articles
        ALTER COLUMN title TYPE VARCHAR(225)
        """
    )
]
