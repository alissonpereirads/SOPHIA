from langchain_community.utilities.sql_database import SQLDatabase


def initialize_db(db_uri):
    db = SQLDatabase.from_uri(db_uri)
    return db
