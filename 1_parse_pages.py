#1_parse_pages.py
import xml.etree.ElementTree as ET

XMLNS = "{http://www.mediawiki.org/xml/export-0.11/}"
tree = ET.parse("enwikiquote-20250601-pages-articles-multistream.xml")
root = tree.getroot()

pages = []
for page in root.findall(f".//{XMLNS}page"):
    title = page.find(f"{XMLNS}title").text
    text_el = page.find(f".//{XMLNS}text")
    text = text_el.text if text_el is not None else ""
    pages.append({"title": title, "text": text})

# Optionally save for inspection
import json
with open("parsed_pages.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, indent=2)
print(f"Extracted {len(pages)} pages")
