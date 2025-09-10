import requests
from bs4 import BeautifulSoup
import os

# Create an output directory if it doesn't exist
output_dir = "crawled_output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Array of URLs to crawl (add your own URLs here)
urls_to_crawl = [
    "https://example.com/page1",
    "https://example.com/page2",
    # Add more URLs as needed
]

def get_plain_text(url):
    """Fetches a URL and returns the plain text content."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text from the body, and remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")
        return None

def save_text_to_file(url, text):
    """Saves the plain text to a file, using the URL's path as the filename."""
    # Create a safe filename from the URL
    filename = os.path.basename(url) + ".txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved text from {url} to {filepath}")

def main():
    """Main function to perform the crawling and saving."""
    for url in urls_to_crawl:
        print(f"Crawling: {url}")
        text_content = get_plain_text(url)
        if text_content:
            save_text_to_file(url, text_content)

if __name__ == "__main__":
    main()
