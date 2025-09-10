import requests
from bs4 import BeautifulSoup
import os

# Configuration for the target website
TARGET_URL = "https://en.wikipedia.org/wiki/Main_Page" # Main page of Wikipedia
URL_PREFIX = "/wiki/" # The prefix for all valid Wikipedia article URLs
URLS_FILE = "urls.txt"

def find_new_urls(target_url, url_prefix):
    """Crawls a target page and finds new URLs matching a prefix."""
    try:
        print(f"Crawling {target_url} for new links...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(target_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        found_urls = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            # Check for the correct prefix and ignore special/system links
            if href and href.startswith(url_prefix) and ":" not in href and "Main_Page" not in href:
                full_url = "https://en.wikipedia.org" + href
                found_urls.add(full_url)
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

    # Find the URLs that are new
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
    discovered_urls = find_new_urls(TARGET_URL, URL_PREFIX)
    if discovered_urls:
        if update_urls_file(discovered_urls):
            return 0 # Success, changes made
    return 1 # No changes, nothing to commit

if __name__ == "__main__":
    import sys
    sys.exit(main())
