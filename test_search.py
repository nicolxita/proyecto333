import urllib.request
import urllib.parse
import re
import json

def get_tiktok_ids(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        links = re.findall(r'href="(.*?)"', html)
        
        tiktok_ids = set()
        for link in links:
            decoded = urllib.parse.unquote(link)
            match = re.search(r'tiktok\.com/@[^/]+/video/(\d+)', decoded)
            if match:
                tiktok_ids.add(match.group(1))
        
        valid = []
        for vid in tiktok_ids:
            oembed_url = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/{vid}"
            try:
                req2 = urllib.request.Request(oembed_url, headers=headers)
                urllib.request.urlopen(req2).read()
                valid.append(vid)
                if len(valid) == 3:
                    break
            except Exception as e:
                pass
        return valid
    except Exception as e:
        print("Error:", e)
        return []

print(get_tiktok_ids('site:tiktok.com "humidificador" llama video'))
