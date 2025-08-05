#2_extract_quotes.py
import mwparserfromhell
import json

with open("parsed_pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

quote_data = []
for page in pages:
    wikicode = mwparserfromhell.parse(page["text"])
    text_nodes = wikicode.filter_text()
    quotes = [str(node).strip() for node in text_nodes if "'''" in str(node)]
    for quote in quotes:
        quote_data.append({"author": page["title"], "quote": quote})

with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quote_data, f, indent=2)
print(f"Extracted {len(quote_data)} quotes")
