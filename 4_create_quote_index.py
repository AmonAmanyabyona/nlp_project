# 4_create_quote_index.py
from neo4j import GraphDatabase

URI = "bolt://localhost:7688"
USER = "neo4j"
PASSWORD = "naturalp"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with driver.session() as session:
    session.run("""
        CREATE FULLTEXT INDEX quoteIndex IF NOT EXISTS FOR (q:Quote) ON EACH [q.text]
    """)

print("Full-text index 'quoteIndex' created successfully.")
