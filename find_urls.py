import requests
from bs4 import BeautifulSoup
import os
import json
from urllib.parse import urljoin, urlparse

# Load target sites from JSON
with open("target_sites.json", "r") as f:
    TARGET_SITES = json.load(f)

URLS_FILE = "urls.txt"

def find_new_urls(target_url):
    """Crawls a target page and finds new URLs within the same domain."""
    try:
        print(f"Crawling {target_url} for new links...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        found_urls = set()
        base_domain = urlparse(target_url).netloc

        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(target_url, href)
            parsed_url = urlparse(full_url)
            
            if parsed_url.netloc == base_domain and parsed_url.scheme in ['http', 'https']:
                clean_url = full_url.split('#')[0]
                found_urls.add(clean_url)

        return found_urls
    except requests.exceptions.RequestException as e:
        print(f"Error finding URLs from {target_url}: {e}")
        return set()

def update_urls_file(new_urls):
    """Adds new, unique URLs to the urls.txt file and returns True if a change was made."""
    existing_urls = set()
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE, "r") as f:
            existing_urls = {line.strip() for line in f.readlines()}

    new_and_unique = new_urls - existing_urls

    if new_and_unique:
        print(f"Found {len(new_and_unique)} new unique URLs. Appending to {URLS_FILE}...")
        with open(URLS_FILE, "a") as f:
            for url in sorted(list(new_and_unique)):
                f.write(f"\n{url}")
        return True
    else:
        print("No new unique URLs found. File will not be changed.")
        return False

def main():
    """Main function to discover and update URLs."""
    total_discovered_urls = set()
    for target_url, url_prefix in TARGET_SITES.items():
        discovered_urls = find_new_urls(target_url)
        total_discovered_urls.update(discovered_urls)

    if total_discovered_urls:
        if update_urls_file(total_discovered_urls):
            return 0
    return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
