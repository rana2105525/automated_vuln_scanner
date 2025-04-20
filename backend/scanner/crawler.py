import requests
from bs4 import BeautifulSoup

def crawl(url):
    urls = set()
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all("a", href=True):
            href = link['href']
            if href.startswith("http"):
                urls.add(href)
            elif href.startswith("/"):
                base_url = "/".join(url.split("/")[:3])
                urls.add(base_url + href)
    except Exception as e:
        print(f"[!] Error crawling {url}: {e}")
    return list(urls)
