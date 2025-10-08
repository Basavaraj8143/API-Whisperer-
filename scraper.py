import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import os

# -----------------------------
# Fetch Function (static only)
# -----------------------------
def fetch_static(url):
    """Fetch page content using simple GET (no Selenium)."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

# -----------------------------
# Parsing Function
# -----------------------------
def parse_content(html, url):
    """Extract title, content, and code blocks from HTML."""
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title else "Untitled"
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all(["p", "h1", "h2", "h3"])]
    codes = [code.get_text("\n", strip=True) for code in soup.find_all(["code", "pre"])]

    content = "\n".join(paragraphs)
    code_examples = [c for c in codes if len(c) > 20]

    return {
        "title": title,
        "url": url,
        "content": content,
        "code_examples": code_examples,
        "scraped_at": datetime.today().strftime("%Y-%m-%d"),
    }

# -----------------------------
# Pagination / Link Extraction
# -----------------------------
def extract_links(base_url, html, limit=5):
    """Extract internal links from the same domain (basic pagination)."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") or base_url in href:
            if not href.startswith("http"):
                href = base_url.rstrip("/") + "/" + href.lstrip("/")
            if href not in links and len(links) < limit:
                links.append(href)
    return links

# -----------------------------
# Master Scraper
# -----------------------------
def scrape_url(start_url, max_pages=3):
    """Scrape a website and return list of parsed pages."""
    visited, docs = set(), []
    to_visit = [start_url]

    for url in tqdm(to_visit[:max_pages], desc="Scraping pages"):
        if url in visited:
            continue
        visited.add(url)

        html = fetch_static(url)
        if not html:
            print(f"❌ Could not scrape {url}")
            continue

        page_data = parse_content(html, url)
        docs.append(page_data)

        # auto-discover new links
        if len(to_visit) < max_pages:
            new_links = extract_links(start_url, html, limit=max_pages)
            for link in new_links:
                if link not in visited:
                    to_visit.append(link)

    return docs

# -----------------------------
# Save Functions
# -----------------------------
def save_to_json(data, filename="output/docs.json"):
    """Save scraped docs to JSON."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    output = {"docs": []}
    for i, d in enumerate(data, 1):
        d["id"] = str(i)
        output["docs"].append(d)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"\n✅ Saved {len(data)} docs → {filename}")

# -----------------------------
# Chunk Creation
# -----------------------------
def create_chunks(docs, chunk_size=800, overlap=100):
    """Split doc content into small overlapping text chunks."""
    chunks = []
    for doc in docs:
        text = doc["content"]
        for i in range(0, len(text), chunk_size - overlap):
            chunk_text = text[i:i+chunk_size]
            chunks.append({
                "id": f"{doc['id']}_{i // (chunk_size - overlap)}",
                "text": chunk_text,
                "source": doc["url"],
                "title": doc["title"]
            })
    return chunks

def save_chunks(chunks, filename="output/chunks.json"):
    """Save text chunks for embeddings."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
    print(f"✅ Saved {len(chunks)} chunks → {filename}")

# -----------------------------
# Main Runner
# -----------------------------
if __name__ == "__main__":
    start_url = "https://api.jquery.com/"  # sample URL
    docs = scrape_url(start_url, max_pages=3)
    save_to_json(docs)

    chunks = create_chunks(docs, chunk_size=800, overlap=100)
    save_chunks(chunks)
