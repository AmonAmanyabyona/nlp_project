# autocomplete_search5.py

from neo4j import GraphDatabase

URI = "bolt://localhost:7688"
USER = "neo4j"
PASSWORD = "naturalp"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def search_quotes(user_input):
    query = """
    CALL db.index.fulltext.queryNodes('quoteIndex', $input)
    YIELD node, score
    OPTIONAL MATCH (a:Author)-[:SAID]->(node)
    RETURN a.name AS author, node.text AS quote, score
    ORDER BY score DESC
    LIMIT 5
    """
    with driver.session() as session:
        results = session.run(query, input=user_input)
        return [{"author": r["author"], "quote": r["quote"], "score": r["score"]} for r in results]

# Run this only if script is executed directly
if __name__ == "__main__":
    phrase = input("Enter a phrase to search for: ")
    matches = search_quotes(phrase)
    if matches:
        print("\n Top matching quotes:\n")
        for match in matches:
            print(f" {match['author']}:")
            print(f"  \"{match['quote']}\"")
            print(f"  (Score: {match['score']:.2f})\n")
    else:
        print("No matching quotes found.")
