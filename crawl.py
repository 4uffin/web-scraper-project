import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

# Define the output directory and URL file
output_dir = "crawled_output"
urls_file = "urls.txt"

# Create the base output directory if it doesn't exist
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
    """Checks if content has changed before saving and returns True if a change occurred.
    Organizes the output into directories based on domain and subdomain.
    """
    try:
        # Parse the URL to get the domain and path
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path_segments = [seg for seg in parsed_url.path.split('/') if seg]

        # Use the domain and path to create the nested directory structure
        # Replace invalid characters for filenames and directory names
        safe_domain = domain.replace(':', '_').replace('.', '_')
        safe_path_segments = [seg.replace('/', '_').replace(':', '_') for seg in path_segments]
        
        # Build the full directory path
        full_dir_path = os.path.join(output_dir, safe_domain, *safe_path_segments)
        
        # Create the directories if they don't exist
        os.makedirs(full_dir_path, exist_ok=True)
        
        # Create a filename based on the final path segment or a default
        if path_segments:
            filename = path_segments[-1] or "index"
        else:
            filename = "index"
        
        # Ensure the filename is safe
        safe_filename = filename.replace('/', '_').replace(':', '_') + ".txt"
        filepath = os.path.join(full_dir_path, safe_filename)

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
    except Exception as e:
        print(f"Error saving {url} to file: {e}")
        return False

def main():
    """Main function to perform the crawling and saving."""
    changes_detected = False
    if not urls_to_crawl:
        print("No URLs found in urls.txt. Please add URLs to the file.")
        return 1
        
    for url in urls_to_crawl:
        print(f"Crawling: {url}")
        text_content = get_plain_text(url)
        if text_content:
            if save_text_if_changed(url, text_content):
                changes_detected = True

    if not changes_detected:
        print("No changes to commit. Exiting.")
        return 1  # A non-zero exit code indicates nothing to commit
    else:
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
