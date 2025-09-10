import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import yaml
import os
import openai
from github import Github
import time

def load_config(config_path='config.yaml'):
    """
    Loads configuration settings from a YAML file.
    
    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: The configuration dictionary.
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_page_content(url):
    """
    Fetches the content of a web page.
    
    Args:
        url (str): The URL of the page.

    Returns:
        str: The HTML content of the page, or None if the request fails.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def find_relevant_links(html_content, openrouter_api_key, topic):
    """
    Uses the OpenRouter API to intelligently find relevant links.
    
    Args:
        html_content (str): The HTML content of the page.
        openrouter_api_key (str): Your OpenRouter API key.
        topic (str): The topic of interest for the crawler.
        
    Returns:
        list: A list of relevant links found on the page.
    """
    # Extract all links and a summary of the page for the LLM
    soup = BeautifulSoup(html_content, 'html.parser')
    all_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    page_text = soup.get_text(separator=' ', strip=True)
    summary = page_text[:2000] # Take a snippet to reduce token usage
    
    # Set up the OpenRouter client
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
        default_headers={"HTTP-Referer": "http://localhost:5000"} # Required by OpenRouter
    )

    # Craft the prompt for the LLM
    prompt = f"""
    You are a web exploration AI. Your task is to analyze a webpage and identify the most relevant links based on a specific topic.
    The topic of interest is: "{topic}".
    The content of the current page is:
    ---
    {summary}
    ---
    The links found on the page are:
    {all_links}
    
    Please return a JSON array of the 5 most relevant links from the provided list that are most likely to contain more information about the topic. If there are fewer than 5 relevant links, return all of them. Do not include external download links or social media links.
    Example response format:
    ["https://example.com/topic-a", "https://example.com/subtopic-b"]
    """
    
    print("Asking OpenRouter for intelligent link selection...")
    try:
        response = client.chat.completions.create(
            model="openrouter/auto", # Use the auto-router to pick the best model
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        json_response = response.choices[0].message.content
        result_json = json.loads(json_response)
        
        return result_json.get("relevant_links", [])
    
    except openai.APIError as e:
        print(f"OpenRouter API error: {e}")
        return []

def output_to_github(repo_owner, repo_name, token, file_name, content, commit_message):
    """
    Commits content to a GitHub repository.
    
    Args:
        repo_owner (str): The owner of the repository.
        repo_name (str): The name of the repository.
        token (str): Your GitHub personal access token.
        file_name (str): The name of the file to create/update.
        content (str): The content to write to the file.
        commit_message (str): The commit message.
        
    Returns:
        bool: True if the commit was successful, False otherwise.
    """
    try:
        g = Github(token)
        user = g.get_user()
        
        # Check if the repository exists, if not, create it
        try:
            repo = g.get_repo(f"{repo_owner}/{repo_name}")
        except Exception:
            print(f"Repository '{repo_name}' not found. Creating it...")
            repo = user.create_repo(repo_name)
            
        # Check if the file exists
        try:
            contents = repo.get_contents(file_name)
            repo.update_file(contents.path, commit_message, content, contents.sha)
            print(f"Successfully updated file '{file_name}' in '{repo_name}'.")
        except Exception:
            repo.create_file(file_name, commit_message, content)
            print(f"Successfully created file '{file_name}' in '{repo_name}'.")
            
        return True
    except Exception as e:
        print(f"Failed to output to GitHub: {e}")
        return False

def main():
    """
    Main function to run the intelligent web crawler.
    """
    # Load configuration from YAML file
    try:
        config = load_config()
    except FileNotFoundError:
        print("Error: config.yaml not found. Please create it first.")
        return
    
    # Extract settings
    start_url = config['crawler']['start_url']
    crawl_depth = config['crawler']['depth']
    topic = config['crawler']['topic']
    
    openrouter_key = config['api_keys']['openrouter']
    
    github_owner = config['github']['repo_owner']
    github_name = config['github']['repo_name']
    github_token = config['github']['token']
    
    # Initialize crawling queue and visited set
    queue = [(start_url, 0)]
    visited = set()
    crawl_summary = []
    
    # Start the crawling process
    while queue:
        current_url, current_depth = queue.pop(0)
        
        # Check if we've already visited this URL or exceeded the depth
        if current_url in visited or current_depth > crawl_depth:
            continue
            
        print(f"Crawling URL: {current_url} (Depth: {current_depth})")
        visited.add(current_url)
        
        # Fetch the page content
        html_content = get_page_content(current_url)
        if not html_content:
            continue
        
        # Use OpenRouter to find relevant links
        relevant_links = find_relevant_links(html_content, openrouter_key, topic)
        
        # Process the relevant links
        if relevant_links:
            print("Found relevant links:")
            for link in relevant_links:
                print(f"  -> {link}")
                # Add the relevant link to the queue for the next crawl depth
                queue.append((link, current_depth + 1))
        
        # Add a summary of the current page to the crawl summary
        soup = BeautifulSoup(html_content, 'html.parser')
        page_title = soup.title.string.strip() if soup.title else 'No Title'
        page_summary = soup.get_text(separator=' ', strip=True)[:500] + '...'
        
        crawl_summary.append({
            'url': current_url,
            'title': page_title,
            'summary': page_summary,
            'relevant_links_followed': relevant_links
        })
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(2)
    
    # Prepare the output content for GitHub
    output_content = "Intelligent Web Crawler Report\n\n"
    output_content += f"Topic: {topic}\n\n"
    output_content += "--- Crawled Pages ---\n\n"
    for page in crawl_summary:
        output_content += f"URL: {page['url']}\n"
        output_content += f"Title: {page['title']}\n"
        output_content += f"Summary: {page['summary']}\n"
        output_content += "Relevant links followed:\n"
        for link in page['relevant_links_followed']:
            output_content += f"  - {link}\n"
        output_content += "\n"
        
    # Output the final report to GitHub
    if output_content:
        output_to_github(
            github_owner,
            github_name,
            github_token,
            'crawl_report.txt',
            output_content,
            'Add intelligent crawler report'
        )

if __name__ == "__main__":
    main()
