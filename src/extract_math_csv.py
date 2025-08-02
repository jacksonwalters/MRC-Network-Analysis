import json
import csv
from pathlib import Path
import ast

INPUT_FILE = Path("data/raw/arxiv-metadata-oai-snapshot.json")
OUTPUT_FILE = Path("data/cleaned/math_arxiv_snapshot.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def is_math_paper(paper):
    return paper.get("categories", "").startswith("math")

def parse_authors(authors_str):
    authors = []
    for name in authors_str.split(","):
        parts = name.strip().split()
        if len(parts) >= 2:
            authors.append([parts[-1], " ".join(parts[:-1])])  # [Last, Firsts]
    return authors

print(f"🔍 Reading: {INPUT_FILE}")
print(f"📤 Writing: {OUTPUT_FILE}")

with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

    writer = None
    paper_count = 0

    for line in infile:
        paper = json.loads(line)
        if is_math_paper(paper):
            authors_str = paper.get("authors", "")
            authors_parsed = parse_authors(authors_str)

            row = {
                "id": paper.get("id"),
                "title": paper.get("title", "").strip(),
                "abstract": paper.get("abstract", "").strip(),
                "categories": paper.get("categories", ""),
                "authors": authors_str,
                "authors_parsed": str(authors_parsed),  # Stored as stringified list
                "update_date": paper.get("update_date", "")
            }

            if writer is None:
                writer = csv.DictWriter(outfile, fieldnames=row.keys())
                writer.writeheader()

            writer.writerow(row)
            paper_count += 1

print(f"✅ Done. Extracted {paper_count} math papers.")
