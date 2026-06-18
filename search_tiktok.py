import urllib.request
import urllib.parse
import re

query = 'site:tiktok.com/video/ "humidificador" llama'
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    links = re.findall(r'href="(https://www\.tiktok\.com/@[^/]+/video/\d+)"', html)
    
    # deduplicate while preserving order
    seen = set()
    unique_links = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    print("FOUND LINKS:")
    for l in unique_links[:5]:
        print(l)
except Exception as e:
    print("Error:", e)
