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
    "https://www.semanticscholar.org/": "https://www.semanticscholar.org/",
    "https://www.nature.com/": "https://www.nature.com/",
    "https://www.science.org/": "https://www.science.org/",
    "https://plos.org/": "https://plos.org/",

    # Blogs and Forums
    "https://www.blogger.com/": "https://www.blogger.com/",
    "https://dev.to/": "https://dev.to/",
    "https://hashnode.com/": "https://hashnode.com/",
    "https://medium.com/": "https://medium.com/",
    "https://quora.com/": "https://quora.com/",
    "https://www.reddit.com/r/programming/": "https://www.reddit.com/",
    "https://www.tripadvisor.com/": "https://www.tripadvisor.com/",
    "https://substack.com/": "https://substack.com/",
    "https://www.tumblr.com/": "https://www.tumblr.com/",
    "https://wordpress.com/": "https://wordpress.com/",
    
    # E-commerce and Popular Sites
    "https://www.amazon.com/": "https://www.amazon.com/",
    "https://www.ebay.com/": "https://www.ebay.com/",
    "https://www.target.com/": "https://www.target.com/",
    "https://www.walmart.com/": "https://www.walmart.com/",
    "https://www.bestbuy.com/": "https://www.bestbuy.com/",
    "https://www.costco.com/": "https://www.costco.com/",
    "https://www.homedepot.com/": "https://www.homedepot.com/",
    "https://www.lowes.com/": "https://www.lowes.com/",
    "https://www.etsy.com/": "https://www.etsy.com/",
    "https://www.shopify.com/": "https://www.shopify.com/",
    
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
    "https://www.youtube.com/": "https://www.youtube.com/",
    "https://www.twitch.tv/": "https://www.twitch.tv/",
    
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
    "https://www.washingtonpost.com/": "https://www.washingtonpost.com/",
    "https://www.wsj.com/": "https://www.wsj.com/",
    "https://www.npr.org/": "https://www.npr.org/",
    "https://www.pbs.org/": "https://www.pbs.org/",
    "https://www.time.com/": "https://www.time.com/",
    "https://www.newsweek.com/": "https://www.newsweek.com/",
    "https://www.axios.com/": "https://www.axios.com/",
    "https://www.politico.com/": "https://www.politico.com/",
    "https://www.thehill.com/": "https://www.thehill.com/",
    "https://www.vox.com/": "https://www.vox.com/",
    "https://www.vice.com/": "https://www.vice.com/",
    "https://www.buzzfeed.com/": "https://www.buzzfeed.com/",
    "https://www.nbcnews.com/": "https://www.nbcnews.com/",
    "https://www.latimes.com/": "https://www.latimes.com/",
    "https://www.sfgate.com/": "https://www.sfgate.com/",
    "https://www.chicagotribune.com/": "https://www.chicagotribune.com/",
    "https://www.economist.com/": "https://www.economist.com/",
    "https://www.ft.com/": "https://www.ft.com/",
    "https://www.theguardian.com/": "https://www.theguardian.com/",
    "https://www.aljazeera.com/": "https://www.aljazeera.com/",
    "https://www.sciencenews.org/": "https://www.sciencenews.org/",
    "https://www.nature.com/news/": "https://www.nature.com/news/",
    "https://www.techcrunch.com/": "https://www.techcrunch.com/",
    "https://www.engadget.com/": "https://www.engadget.com/",
    "https://www.wired.com/": "https://www.wired.com/",
    "https://www.slashdot.org/": "https://www.slashdot.org/",
    "https://www.theverge.com/": "https://www.theverge.com/",
    "https://www.mashable.com/": "https://www.mashable.com/",
    "https://arstechnica.com/": "https://arstechnica.com/",
    "https://www.politifact.com/": "https://www.politifact.com/",
    "https://www.snopes.com/": "https://www.snopes.com/",
    "https://www.propublica.org/": "https://www.propublica.org/",
    "https://www.scientificamerican.com/": "https://www.scientificamerican.com/",
    "https://www.nationalgeographic.com/": "https://www.nationalgeographic.com/",
    "https://www.bostonglobe.com/": "https://www.bostonglobe.com/",
    "https://www.dw.com/": "https://www.dw.com/",
    "https://globalnews.ca/": "https://globalnews.ca/",
    "https://www.cbc.ca/news": "https://www.cbc.ca/news",
    "https://www.smh.com.au/": "https://www.smh.com.au/",
    "https://www.japantimes.co.jp/": "https://www.japantimes.co.jp/",
    "https://www.lemonde.fr/": "https://www.lemonde.fr/",
    "https://www.elpais.com/": "https://www.elpais.com/",
    "https://www.independent.co.uk/": "https://www.independent.co.uk/",
    "https://www.thedailybeast.com/": "https://www.thedailybeast.com/",
    "https://www.newyorker.com/": "https://www.newyorker.com/",
    
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
    "https://www.wired.com/": "https://www.wired.com/",
    "https://www.engadget.com/": "https://www.engadget.com/",
    "https://www.tomshardware.com/": "https://www.tomshardware.com/",
    "https://www.anandtech.com/": "https://www.anandtech.com/",
    "https://www.pcworld.com/": "https://www.pcworld.com/",
    "https://www.computerworld.com/": "https://www.computerworld.com/",
    "https://www.infoworld.com/": "https://www.infoworld.com/",
    "https://www.zdnet.com/": "https://www.zdnet.com/",
    "https://www.techmeme.com/": "https://www.techmeme.com/",
    "https://slashdot.org/": "https://slashdot.org/",
    "https://www.hackernoon.com/": "https://www.hackernoon.com/",
    "https://www.dzone.com/": "https://www.dzone.com/",
    "https://css-tricks.com/": "https://css-tricks.com/",
    "https://codepen.io/": "https://codepen.io/",
    "https://jsfiddle.net/": "https://jsfiddle.net/",
    "https://replit.com/": "https://replit.com/",
    "https://codesandbox.io/": "https://codesandbox.io/",
    "https://glitch.com/": "https://glitch.com/",
    "https://www.hackerrank.com/": "https://www.hackerrank.com/",
    "https://leetcode.com/": "https://leetcode.com/",
    "https://www.codewars.com/": "https://www.codewars.com/",
    "https://www.topcoder.com/": "https://www.topcoder.com/",
    "https://codeforces.com/": "https://codeforces.com/",
    
    # AI and Machine Learning
    "https://pytorch.org/": "https://pytorch.org/",
    "https://scikit-learn.org/": "https://scikit-learn.org/",
    "https://www.kaggle.com/": "https://www.kaggle.com/",
    "https://papers.withcode.com/": "https://papers.withcode.com/",
    "https://distill.pub/": "https://distill.pub/",
    "https://towardsdatascience.com/": "https://towardsdatascience.com/",
    "https://machinelearningmastery.com/": "https://machinelearningmastery.com/",
    "https://www.deeplearning.ai/": "https://www.deeplearning.ai/",
    "https://deepmind.com/": "https://deepmind.com/",
    "https://ai.google/": "https://ai.google/",
    
    # Cloud and DevOps
    "https://aws.amazon.com/": "https://aws.amazon.com/",
    "https://cloud.google.com/": "https://cloud.google.com/",
    "https://azure.microsoft.com/": "https://azure.microsoft.com/",
    "https://www.digitalocean.com/": "https://www.digitalocean.com/",
    "https://www.linode.com/": "https://www.linode.com/",
    "https://www.vultr.com/": "https://www.vultr.com/",
    "https://www.heroku.com/": "https://www.heroku.com/",
    "https://vercel.com/": "https://vercel.com/",
    "https://netlify.com/": "https://netlify.com/",
    "https://www.docker.com/": "https://www.docker.com/",
    
    # Design and Creative
    "https://www.behance.net/": "https://www.behance.net/",
    "https://dribbble.com/": "https://dribbble.com/",
    "https://www.figma.com/": "https://www.figma.com/",
    "https://www.adobe.com/": "https://www.adobe.com/",
    "https://www.canva.com/": "https://www.canva.com/",
    "https://unsplash.com/": "https://unsplash.com/",
    "https://www.pexels.com/": "https://www.pexels.com/",
    "https://pixabay.com/": "https://pixabay.com/",
    "https://www.shutterstock.com/": "https://www.shutterstock.com/",
    "https://www.gettyimages.com/": "https://www.gettyimages.com/",
    
    # Finance and Business
    "https://www.investopedia.com/": "https://www.investopedia.com/",
    "https://finance.yahoo.com/": "https://finance.yahoo.com/",
    "https://www.marketwatch.com/": "https://www.marketwatch.com/",
    "https://www.fool.com/": "https://www.fool.com/",
    "https://www.morningstar.com/": "https://www.morningstar.com/",
    "https://www.sec.gov/": "https://www.sec.gov/",
    "https://www.nasdaq.com/": "https://www.nasdaq.com/",
    "https://www.nyse.com/": "https://www.nyse.com/",
    "https://www.entrepreneur.com/": "https://www.entrepreneur.com/",
    "https://www.inc.com/": "https://www.inc.com/",
    "https://hbr.org/": "https://hbr.org/",
    "https://www.fastcompany.com/": "https://www.fastcompany.com/",
    "https://www.businessinsider.com/": "https://www.businessinsider.com/",
    "https://www.cnbc.com/business/": "https://www.cnbc.com/business/",
    "https://www.barrons.com/": "https://www.barrons.com/",
    "https://www.bloomberg.com/businessweek": "https://www.bloomberg.com/businessweek",
    "https://www.wsj.com/": "https://www.wsj.com/",
    "https://www.economist.com/": "https://www.economist.com/",
    "https://www.ft.com/": "https://www.ft.com/",
    "https://www.reuters.com/business/": "https://www.reuters.com/business/",
    "https://www.forbes.com/business/": "https://www.forbes.com/business/",
    "https://www.investing.com/": "https://www.investing.com/",
    "https://www.seekingalpha.com/": "https://www.seekingalpha.com/",
    "https://www.kiplinger.com/": "https://www.kiplinger.com/",
    "https://www.nerdwallet.com/": "https://www.nerdwallet.com/",
    "https://www.creditkarma.com/": "https://www.creditkarma.com/",
    "https://www.bankrate.com/": "https://www.bankrate.com/",
    "https://www.valuepenguin.com/": "https://www.valuepenguin.com/",
    "https://www.sba.gov/": "https://www.sba.gov/",
    "https://www.worldbank.org/": "https://www.worldbank.org/",
    "https://www.imf.org/": "https://www.imf.org/",
    "https://www.oecd.org/": "https://www.oecd.org/",
    "https://www.crowdfundinsider.com/": "https://www.crowdfundinsider.com/",
    "https://www.cbinsights.com/": "https://www.cbinsights.com/",
    "https://www.crunchbase.com/": "https://www.crunchbase.com/",
    "https://pitchbook.com/": "https://pitchbook.com/",
    "https://angel.co/": "https://angel.co/",
    "https://www.macrotrends.net/": "https://www.macrotrends.net/",
    "https://www.federalreserve.gov/": "https://www.federalreserve.gov/",
    "https://fred.stlouisfed.org/": "https://fred.stlouisfed.org/",
    "https://www.spglobal.com/": "https://www.spglobal.com/",
    "https://www.moody's.com/": "https://www.moody's.com/",
    "https://www.statista.com/": "https://www.statista.com/",
    "https://www.privco.com/": "https://www.privco.com/",
    "https://www.plainsite.org/": "https://www.plainsite.org/",
    "https://www.edgar-online.com/": "https://www.edgar-online.com/",
    
    # Health and Lifestyle
    "https://www.webmd.com/": "https://www.webmd.com/",
    "https://www.mayoclinic.org/": "https://www.mayoclinic.org/",
    "https://www.healthline.com/": "https://www.healthline.com/",
    "https://www.medicalnewstoday.com/": "https://www.medicalnewstoday.com/",
    "https://www.nih.gov/": "https://www.nih.gov/",
    "https://www.cdc.gov/": "https://www.cdc.gov/",
    "https://www.who.int/": "https://www.who.int/",
    "https://www.goodhousekeeping.com/": "https://www.goodhousekeeping.com/",
    "https://www.allrecipes.com/": "https://www.allrecipes.com/",
    "https://www.foodnetwork.com/": "https://www.foodnetwork.com/",
    
    # Travel and Geography
    "https://www.booking.com/": "https://www.booking.com/",
    "https://www.expedia.com/": "https://www.expedia.com/",
    "https://www.airbnb.com/": "https://www.airbnb.com/",
    "https://www.kayak.com/": "https://www.kayak.com/",
    "https://www.skyscanner.com/": "https://www.skyscanner.com/",
    "https://www.lonelyplanet.com/": "https://www.lonelyplanet.com/",
    "https://www.nationalgeographic.com/": "https://www.nationalgeographic.com/",
    "https://www.atlasobscura.com/": "https://www.atlasobscura.com/",
    "https://www.tripadvisor.com/": "https://www.tripadvisor.com/",
    "https://www.trivago.com/": "https://www.trivago.com/",
    
    # Utilities and Tools
    "https://archive.org/": "https://archive.org/",
    "https://maps.google.com/": "https://maps.google.com/",
    "https://www.google.com/": "https://www.google.com/",
    "https://www.bing.com/": "https://www.bing.com/",
    "https://duckduckgo.com/": "https://duckduckgo.com/",
    "https://www.wolframalpha.com/": "https://www.wolframalpha.com/",
    "https://pastebin.com/": "https://pastebin.com/",
    "https://gist.github.com/": "https://gist.github.com/",
    "https://www.timeanddate.com/": "https://www.timeanddate.com/",
    "https://www.worldclock.com/": "https://www.worldclock.com/",
    "https://codebeautify.org/": "https://codebeautify.org/",
    "https://www.random.org/": "https://www.random.org/",
    "https://www.bitly.com/": "https://www.bitly.com/",
    "https://www.tinyurl.com/": "https://www.tinyurl.com/",
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
