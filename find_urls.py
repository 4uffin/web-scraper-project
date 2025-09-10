import requests
from bs4 import BeautifulSoup
import os

# Configuration for the target website
TARGET_URL = "https://example.com/blog" # Replace with your target URL
URL_PREFIX = "https://example.com/articles/" # Replace with the prefix of the URLs you want to find
URLS_FILE = "urls.txt"

def find_new_urls(target_url, url_prefix):
    """Crawls a target page and finds new URLs matching a prefix."""
    try:
        print(f"Crawling {target_url} for new links...")
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        found_urls = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and href.startswith(url_prefix):
                found_urls.add(href)
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
            return 0  # Success, changes made
    return 1  # No changes, nothing to commit

if __name__ == "__main__":
    import sys
    sys.exit(main())
