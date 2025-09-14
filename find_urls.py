import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# Configuration for multiple target websites
TARGET_SITES = {
    # Academic and Research
    "https://arxiv.org/": "https://arxiv.org/",
    "https://eric.ed.gov/": "https://eric.ed.gov/",
    "https://www.jstor.org/": "https://www.jstor.org/",
    "https://pubmed.ncbi.nlm.nih.gov/": "https://pubmed.ncbi.nlm.nih.gov/",
    "https://www.researchgate.net/": "https://www.researchgate.net/",
    "https://scholar.google.com/": "https://scholar.google.com/",
    # Blogs and Forums
    "https://www.blogger.com/": "https://www.blogger.com/",
    "https://dev.to/": "https://dev.to/",
    "https://hashnode.com/": "https://hashnode.com/",
    "https://medium.com/": "https://medium.com/",
    "https://quora.com/": "https://quora.com/",
    "https://www.reddit.com/r/programming/": "https://www.reddit.com/",
    "https://www.tripadvisor.com/": "https://www.tripadvisor.com/",
    # E-commerce and Popular Sites
    "https://www.amazon.com/": "https://www.amazon.com/",
    "https://www.ebay.com/": "https://www.ebay.com/",
    "https://www.target.com/": "https://www.target.com/",
    "https://www.walmart.com/": "https://www.walmart.com/",
    # Educational and Reference
    "https://www.codecademy.com/": "https://www.codecademy.com/",
    "https://www.coursera.org/": "https://www.coursera.org/",
    "https://developer.mozilla.org/en-US/": "https://developer.mozilla.org/",
    "https://docs.python.org/3/": "https://docs.python.org/",
    "https://www.edx.org/": "https://www.edx.org/",
    "https://www.freecodecamp.org/": "https://www.freecodecamp.org/",
    "https://www.geeksforgeeks.org/": "https://www.geeksforgeeks.org/",
    "https://www.khanacademy.org/": "https://www.khanacademy.org/",
    "https://www.udemy.com/": "https://www.udemy.com/",
    "https://www.w3schools.com/": "https://www.w3schools.com/",
    # Entertainment and Social
    "https://www.cnet.com/": "https://www.cnet.com/",
    "https://www.gamespot.com/": "https://www.gamespot.com/",
    "https://www.ign.com/": "https://www.ign.com/",
    "https://www.imdb.com/": "https://www.imdb.com/",
    "https://www.instagram.com/": "https://www.instagram.com/",
    "https://www.pinterest.com/": "https://www.pinterest.com/",
    "https://www.rottentomatoes.com/": "https://www.rottentomatoes.com/",
    "https://www.tiktok.com/": "https://www.tiktok.com/",
    # News and Media
    "https://abcnews.go.com/": "https://abcnews.go.com/",
    "https://www.apnews.com/": "https://www.apnews.com/",
    "https://www.bbc.com/news": "https://www.bbc.com/",
    "https://www.bloomberg.com/": "https://www.bloomberg.com/",
    "https://www.cbsnews.com/": "https://www.cbsnews.com/",
    "https://www.cnn.com/": "https://www.cnn.com/",
    "https://www.cnbc.com/": "https://www.cnbc.com/",
    "https://www.forbes.com/": "https://www.forbes.com/",
    "https://www.huffpost.com/": "https://www.huffpost.com/",
    "https://www.nytimes.com/": "https://www.nytimes.com/",
    "https://www.reuters.com/": "https://www.reuters.com/",
    "https://www.usatoday.com/": "https://www.usatoday.com/",
    # Technology and Programming Sites
    "https://arstechnica.com/": "https://arstechnica.com/",
    "https://www.bleepingcomputer.com/": "https://www.bleepingcomputer.com/",
    "https://github.com/trending": "https://github.com/",
    "https://kernel.org/": "https://www.kernel.org/",
    "https://www.linuxquestions.org/": "https://www.linuxquestions.org/",
    "https://www.maketecheasier.com/": "https://www.maketecheasier.com/",
    "https://news.ycombinator.com/": "https://news.ycombinator.com/",
    "https://stackoverflow.com/": "https://stackoverflow.com/",
    "https://techcrunch.com/": "https://techcrunch.com/",
    "https://www.theverge.com/": "https://www.theverge.com/",
    "https://en.wikipedia.org/wiki/Main_Page": "https://en.wikipedia.org/wiki/",
    "https://xda-developers.com/": "https://xda-developers.com/",
}

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
            # Handle different types of links
            full_url = urljoin(target_url, href)
            parsed_url = urlparse(full_url)
            
            # Check for same domain and valid scheme
            if parsed_url.netloc == base_domain and parsed_url.scheme in ['http', 'https']:
                # Clean up the URL by removing fragments (#)
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
            return 0  # Success, changes made
    return 1  # No changes, nothing to commit

if __name__ == "__main__":
    import sys
    sys.exit(main())
