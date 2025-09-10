import requests
from bs4 import BeautifulSoup
import os

# Define the output directory and URL file
output_dir = "crawled_output"
urls_file = "urls.txt"

# Create directories if they don't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read URLs from urls.txt
urls_to_crawl = []
if os.path.exists(urls_file):
    with open(urls_file, "r") as f:
        urls_to_crawl = [line.strip() for line in f.readlines() if line.strip()]

def get_plain_text(url):
    """Fetches a URL with a User-Agent header and returns the plain text."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = "\n".join(chunk for chunk in chunks if chunk)
        return cleaned_text
    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")
        return None

def save_text_if_changed(url, new_text):
    """Checks if content has changed before saving and returns True if a change occurred."""
    filename = os.path.basename(url) + ".txt"
    filepath = os.path.join(output_dir, filename)

    # Check for existing file and compare content
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            old_text = f.read()
            if old_text == new_text:
                print(f"No changes detected for {url}. Skipping.")
                return False

    # Save the new text if it's different or if the file doesn't exist
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"Saved updated text from {url} to {filepath}")
    return True

def main():
    """Main function to perform the crawling and saving."""
    changes_detected = False
    for url in urls_to_crawl:
        print(f"Crawling: {url}")
        text_content = get_plain_text(url)
        if text_content:
            if save_text_if_changed(url, text_content):
                changes_detected = True

    if not changes_detected:
        print("No changes to commit. Exiting.")
        # This will be used by the GitHub Action to decide whether to commit
        return 1  # A non-zero exit code indicates nothing to commit
    else:
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
