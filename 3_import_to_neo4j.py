# 3_import_to_neo4j.py
from neo4j import GraphDatabase
import json

# Connection credentials
URI = "bolt://localhost:7688"
USER = "neo4j"
PASSWORD = "naturalp"

# Initialize Neo4j driver
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# Normalize quotes to reduce duplication risk
def clean_quote(text):
    text = text.strip()                    # Remove leading/trailing whitespace
    text = text.replace("'''", "")         # Remove bold markup
    text = text.replace('\n', ' ').strip() # Flatten to single line
    return text

# Import transaction function
def insert_quote(tx, author, quote):
    quote = clean_quote(quote)
    if not quote: return  # Skip empty quotes
    tx.run("""
        MERGE (a:Author {name: $author})
        MERGE (q:Quote {text: $quote})
        MERGE (a)-[:SAID]->(q)
    """, author=author, quote=quote)

# Read quotes from file
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Start session and insert quotes
with driver.session() as session:
    count = 0
    for item in quotes:
        session.write_transaction(insert_quote, item["author"], item["quote"])
        count += 1

print(f"Imported {count} quotes into Neo4j.")


# MATCH (n:Author)
# RETURN count(n) AS authorCount
#the total is 982
# MATCH (n:Quote)
# RETURN count(n) AS quoteCount
#the total is 1193

#to get author with most quotes but wasn't useful
# MATCH (a:Author)-[:SAID]->(:Quote)
# RETURN a.name AS author, count(*) AS quoteCount
# ORDER BY quoteCount DESC
# LIMIT 1
