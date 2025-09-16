import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# Configuration for multiple target websites
TARGET_SITES = {
    # Academic and Research
    "https://academic.oup.com/": "https://academic.oup.com/",
    "https://arxiv.org/": "https://arxiv.org/",
    "https://www.cambridge.org/": "https://www.cambridge.org/",
    "https://www.cell.com/": "https://www.cell.com/",
    "https://eric.ed.gov/": "https://eric.ed.gov/",
    "https://www.jstor.org/": "https://www.jstor.org/",
    "https://pubmed.ncbi.nlm.nih.gov/": "https://pubmed.ncbi.nlm.nih.gov/",
    "https://www.researchgate.net/": "https://www.researchgate.net/",
    "https://scholar.google.com/": "https://scholar.google.com/",
    "https://www.science.org/": "https://www.science.org/",
    "https://www.semanticscholar.org/": "https://www.semanticscholar.org/",
    "https://www.springer.com/": "https://www.springer.com/",
    "https://www.tandfonline.com/": "https://www.tandfonline.com/",
    "https://www.nature.com/": "https://www.nature.com/",
    "https://plos.org/": "https://plos.org/",
    
    # AI and Machine Learning
    "https://distill.pub/": "https://distill.pub/",
    "https://huggingface.co/": "https://huggingface.co/",
    "https://machinelearningmastery.com/": "https://machinelearningmastery.com/",
    "https://www.anthropic.com/": "https://www.anthropic.com/",
    "https://www.cohere.com/": "https://www.cohere.com/",
    "https://www.deeplearning.ai/": "https://www.deeplearning.ai/",
    "https://www.kaggle.com/": "https://www.kaggle.com/",
    "https://openai.com/": "https://openai.com/",
    "https://papers.withcode.com/": "https://papers.withcode.com/",
    "https://pytorch.org/": "https://pytorch.org/",
    "https://scikit-learn.org/": "https://scikit-learn.org/",
    "https://www.tensorflow.org/": "https://www.tensorflow.org/",
    "https://towardsdatascience.com/": "https://towardsdatascience.com/",
    
    # Blogs and Forums
    "https://dev.to/": "https://dev.to/",
    "https://ghost.org/": "https://ghost.org/",
    "https://hashnode.com/": "https://hashnode.com/",
    "https://medium.com/": "https://medium.com/",
    "https://quora.com/": "https://quora.com/",
    "https://slashdot.org/": "https://slashdot.org/",
    "https://substack.com/": "https://substack.com/",
    "https://www.blogger.com/": "https://www.blogger.com/",
    "https://www.reddit.com/r/programming/": "https://www.reddit.com/",
    "https://www.tumblr.com/": "https://www.tumblr.com/",
    "https://wordpress.com/": "https://wordpress.com/",
    "https://www.tripadvisor.com/": "https://www.tripadvisor.com/",
    "https://news.ycombinator.com/": "https://news.ycombinator.com/",
    
    # Cloud and DevOps
    "https://aws.amazon.com/": "https://aws.amazon.com/",
    "https://azure.microsoft.com/": "https://azure.microsoft.com/",
    "https://bitbucket.org/": "https://bitbucket.org/",
    "https://cloud.google.com/": "https://cloud.google.com/",
    "https://www.digitalocean.com/": "https://www.digitalocean.com/",
    "https://www.docker.com/": "https://www.docker.com/",
    "https://github.com/actions": "https://github.com/",
    "https://gitlab.com/": "https://gitlab.com/",
    "https://www.heroku.com/": "https://www.heroku.com/",
    "https://www.jenkins.io/": "https://www.jenkins.io/",
    "https://kubernetes.io/": "https://kubernetes.io/",
    "https://netlify.com/": "https://netlify.com/",
    "https://vercel.com/": "https://vercel.com/",
    "https://www.linode.com/": "https://www.linode.com/",
    "https://www.vultr.com/": "https://www.vultr.com/",
    
    # Cybersecurity
    "https://www.csoonline.com/": "https://www.csoonline.com/",
    "https://www.darkreading.com/": "https://www.darkreading.com/",
    "https://www.kaspersky.com/": "https://www.kaspersky.com/",
    "https://www.mcafee.com/": "https://www.mcafee.com/",
    "https://www.sans.org/": "https://www.sans.org/",
    
    # Design and Creative
    "https://dribbble.com/": "https://dribbble.com/",
    "https://www.adobe.com/": "https://www.adobe.com/",
    "https://www.behance.net/": "https://www.behance.net/",
    "https://www.canva.com/": "https://www.canva.com/",
    "https://www.figma.com/": "https://www.figma.com/",
    "https://www.gettyimages.com/": "https://www.gettyimages.com/",
    "https://pixabay.com/": "https://pixabay.com/",
    "https://www.pexels.com/": "https://www.pexels.com/",
    "https://unsplash.com/": "https://unsplash.com/",
    "https://www.shutterstock.com/": "https://www.shutterstock.com/",
    
    # Educational and Reference
    "https://brilliant.org/": "https://brilliant.org/",
    "https://www.codecademy.com/": "https://www.codecademy.com/",
    "https://www.coursera.org/": "https://www.coursera.org/",
    "https://developer.mozilla.org/en-US/": "https://developer.mozilla.org/",
    "https://docs.python.org/3/": "https://docs.python.org/",
    "https://www.edx.org/": "https://www.edx.org/",
    "https://www.freecodecamp.org/": "https://www.freecodecamp.org/",
    "https://www.geeksforgeeks.org/": "https://www.geeksforgeeks.org/",
    "https://www.khanacademy.org/": "https://www.khanacademy.org/",
    "https://www.lynda.com/": "https://www.lynda.com/",
    "https://ocw.mit.edu/": "https://ocw.mit.edu/",
    "https://www.pluralsight.com/": "https://www.pluralsight.com/",
    "https://www.skillshare.com/": "https://www.skillshare.com/",
    "https://www.udacity.com/": "https://www.udacity.com/",
    "https://www.udemy.com/": "https://www.udemy.com/",
    "https://www.w3schools.com/": "https://www.w3schools.com/",
    "https://www.masterclass.com/": "https://www.masterclass.com/",
    "https://www.duolingo.com/": "https://www.duolingo.com/",
    
    # E-commerce and Popular Sites
    "https://www.alibaba.com/": "https://www.alibaba.com/",
    "https://www.aliexpress.com/": "https://www.aliexpress.com/",
    "https://www.amazon.com/": "https://www.amazon.com/",
    "https://www.bestbuy.com/": "https://www.bestbuy.com/",
    "https://www.costco.com/": "https://www.costco.com/",
    "https://www.etsy.com/": "https://www.etsy.com/",
    "https://www.homedepot.com/": "https://www.homedepot.com/",
    "https://www.lowes.com/": "https://www.lowes.com/",
    "https://www.newegg.com/": "https://www.newegg.com/",
    "https://www.overstock.com/": "https://www.overstock.com/",
    "https://www.shopify.com/": "https://www.shopify.com/",
    "https://www.target.com/": "https://www.target.com/",
    "https://www.walmart.com/": "https://www.walmart.com/",
    "https://www.zappos.com/": "https://www.zappos.com/",
    "https://www.ebay.com/": "https://www.ebay.com/",
    
    # Entertainment and Social
    "https://www.cnet.com/": "https://www.cnet.com/",
    "https://www.discord.com/": "https://www.discord.com/",
    "https://www.epicgames.com/": "https://www.epicgames.com/",
    "https://www.gamespot.com/": "https://www.gamespot.com/",
    "https://www.ign.com/": "https://www.ign.com/",
    "https://www.imdb.com/": "https://www.imdb.com/",
    "https://kotaku.com/": "https://kotaku.com/",
    "https://letterboxd.com/": "https://letterboxd.com/",
    "https://www.netflix.com/": "https://www.netflix.com/",
    "https://www.pinterest.com/": "https://www.pinterest.com/",
    "https://www.polygon.com/": "https://www.polygon.com/",
    "https://www.rottentomatoes.com/": "https://www.rottentomatoes.com/",
    "https://www.spotify.com/": "https://www.spotify.com/",
    "https://store.steampowered.com/": "https://store.steampowered.com/",
    "https://www.tiktok.com/": "https://www.tiktok.com/",
    "https://www.twitch.tv/": "https://www.twitch.tv/",
    "https://www.youtube.com/": "https://www.youtube.com/",
    "https://www.hulu.com/": "https://www.hulu.com/",
    "https://www.instagram.com/": "https://www.instagram.com/",
    
    # Finance and Business
    "https://www.businessinsider.com/": "https://www.businessinsider.com/",
    "https://www.entrepreneur.com/": "https://www.entrepreneur.com/",
    "https://www.fastcompany.com/": "https://www.fastcompany.com/",
    "https://www.fool.com/": "https://www.fool.com/",
    "https://hbr.org/": "https://hbr.org/",
    "https://www.inc.com/": "https://www.inc.com/",
    "https://www.investopedia.com/": "https://www.investopedia.com/",
    "https://www.marketwatch.com/": "https://www.marketwatch.com/",
    "https://www.morningstar.com/": "https://www.morningstar.com/",
    "https://www.nasdaq.com/": "https://www.nasdaq.com/",
    "https://www.nyse.com/": "https://www.nyse.com/",
    "https://www.sec.gov/": "https://www.sec.gov/",
    "https://finance.yahoo.com/": "https://finance.yahoo.com/",
    
    # Government and Legal
    "https://www.congress.gov/": "https://www.congress.gov/",
    "https://www.epa.gov/": "https://www.epa.gov/",
    "https://www.fbi.gov/": "https://www.fbi.gov/",
    "https://www.fda.gov/": "https://www.fda.gov/",
    "https://www.irs.gov/": "https://www.irs.gov/",
    "https://www.supremecourt.gov/": "https://www.supremecourt.gov/",
    "https://www.usa.gov/": "https://www.usa.gov/",
    "https://www.whitehouse.gov/": "https://www.whitehouse.gov/",
    
    # Health and Lifestyle
    "https://www.allrecipes.com/": "https://www.allrecipes.com/",
    "https://www.cdc.gov/": "https://www.cdc.gov/",
    "https://www.epicurious.com/": "https://www.epicurious.com/",
    "https://www.foodnetwork.com/": "https://www.foodnetwork.com/",
    "https://www.goodhousekeeping.com/": "https://www.goodhousekeeping.com/",
    "https://www.healthline.com/": "https://www.healthline.com/",
    "https://www.mayoclinic.org/": "https://www.mayoclinic.org/",
    "https://www.medicalnewstoday.com/": "https://www.medicalnewstoday.com/",
    "https://www.nih.gov/": "https://www.nih.gov/",
    "https://www.tasteofhome.com/": "https://www.tasteofhome.com/",
    "https://www.webmd.com/": "https://www.webmd.com/",
    "https://www.who.int/": "https://www.who.int/",
    
    # News and Media
    "https://abcnews.go.com/": "https://abcnews.go.com/",
    "https://www.aljazeera.com/": "https://www.aljazeera.com/",
    "https://www.apnews.com/": "https://www.apnews.com/",
    "https://www.axios.com/": "https://www.axios.com/",
    "https://www.bbc.com/news": "https://www.bbc.com/",
    "https://www.bloomberg.com/": "https://www.bloomberg.com/",
    "https://www.buzzfeed.com/": "https://www.buzzfeed.com/",
    "https://www.cbsnews.com/": "https://www.cbsnews.com/",
    "https://www.cnbc.com/": "https://www.cnbc.com/",
    "https://www.cnn.com/": "https://www.cnn.com/",
    "https://www.forbes.com/": "https://www.forbes.com/",
    "https://www.guardian.com/": "https://www.guardian.com/",
    "https://www.huffpost.com/": "https://www.huffpost.com/",
    "https://www.npr.org/": "https://www.npr.org/",
    "https://www.nytimes.com/": "https://www.nytimes.com/",
    "https://www.pbs.org/": "https://www.pbs.org/",
    "https://www.politico.com/": "https://www.politico.com/",
    "https://www.reuters.com/": "https://www.reuters.com/",
    "https://www.thehill.com/": "https://www.thehill.com/",
    "https://www.time.com/": "https://www.time.com/",
    "https://www.usatoday.com/": "https://www.usatoday.com/",
    "https://www.vox.com/": "https://www.vox.com/",
    "https://www.washingtonpost.com/": "https://www.washingtonpost.com/",
    "https://www.wsj.com/": "https://www.wsj.com/",
    "https://www.newsweek.com/": "https://www.newsweek.com/",
    "https://www.vice.com/": "https://www.vice.com/",
    
    # Open Source Foundations
    "https://www.apache.org/": "https://www.apache.org/",
    "https://www.gnu.org/": "https://www.gnu.org/",
    "https://www.linuxfoundation.org/": "https://www.linuxfoundation.org/",
    "https://www.mozilla.org/": "https://www.mozilla.org/",
    
    # Science and Space
    "https://www.esa.int/": "https://www.esa.int/",
    "https://www.jpl.nasa.gov/": "https://www.jpl.nasa.gov/",
    "https://www.nasa.gov/": "https://www.nasa.gov/",
    "https://www.nationalgeographic.com/science": "https://www.nationalgeographic.com/science",
    "https://www.spacex.com/": "https://www.spacex.com/",
    
    # Sports
    "https://www.espn.com/": "https://www.espn.com/",
    "https://www.fifa.com/": "https://www.fifa.com/",
    "https://www.mlb.com/": "https://www.mlb.com/",
    "https://www.nba.com/": "https://www.nba.com/",
    "https://www.nfl.com/": "https://www.nfl.com/",
    "https://www.nhl.com/": "https://www.nhl.com/",
    "https://www.olympics.com/": "https://www.olympics.com/",
    
    # Technology and Programming
    "https://arstechnica.com/": "https://arstechnica.com/",
    "https://www.anandtech.com/": "https://www.anandtech.com/",
    "https://www.bleepingcomputer.com/": "https://www.bleepingcomputer.com/",
    "https://codeforces.com/": "https://codeforces.com/",
    "https://www.codewars.com/": "https://www.codewars.com/",
    "https://codesandbox.io/": "https://codesandbox.io/",
    "https://css-tricks.com/": "https://css-tricks.com/",
    "https://www.computerworld.com/": "https://www.computerworld.com/",
    "https://www.dzone.com/": "https://www.dzone.com/",
    "https://www.engadget.com/": "https://www.engadget.com/",
    "https://www.hackernoon.com/": "https://www.hackernoon.com/",
    "https://www.hackerrank.com/": "https://www.hackerrank.com/",
    "https://jsfiddle.net/": "https://jsfiddle.net/",
    "https://leetcode.com/": "https://leetcode.com/",
    "https://www.linuxquestions.org/": "https://www.linuxquestions.org/",
    "https://www.maketecheasier.com/": "https://www.maketecheasier.com/",
    "https://www.pcworld.com/": "https://www.pcworld.com/",
    "https://www.stackoverflow.com/": "https://www.stackoverflow.com/",
    "https://techcrunch.com/": "https://techcrunch.com/",
    "https://www.theverge.com/": "https://www.theverge.com/",
    "https://www.tomshardware.com/": "https://www.tomshardware.com/",
    "https://topcoder.com/": "https://topcoder.com/",
    "https://www.wired.com/": "https://www.wired.com/",
    "https://www.zdnet.com/": "https://www.zdnet.com/",
    
    # Travel and Geography
    "https://www.airbnb.com/": "https://www.airbnb.com/",
    "https://www.atlasobscura.com/": "https://www.atlasobscura.com/",
    "https://www.booking.com/": "https://www.booking.com/",
    "https://www.expedia.com/": "https://www.expedia.com/",
    "https://www.kayak.com/": "https://www.kayak.com/",
    "https://www.lonelyplanet.com/": "https://www.lonelyplanet.com/",
    "https://www.nationalgeographic.com/": "https://www.nationalgeographic.com/",
    "https://www.skyscanner.com/": "https://www.skyscanner.com/",
    
    # Utilities and Tools
    "https://archive.org/": "https://archive.org/",
    "https://www.bing.com/": "https://www.bing.com/",
    "https://duckduckgo.com/": "https://duckduckgo.com/",
    "https://gist.github.com/": "https://gist.github.com/",
    "https://www.google.com/": "https://www.google.com/",
    "https://maps.google.com/": "https://maps.google.com/",
    "https://pastebin.com/": "https://pastebin.com/",
    "https://translate.google.com/": "https://translate.google.com/",
    "https://www.wolframalpha.com/": "https://www.wolframalpha.com/",
    "https://www.mathway.com/": "https://www.mathway.com/",
    "https://www.grammarly.com/": "https://www.grammarly.com/",
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
