import urllib.request
import urllib.parse
import re

query = 'site:tiktok.com "humidificador" llama video'
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)

# We must use a better user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
req = urllib.request.Request(url, headers=headers)
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # In duckduckgo html, urls are often inside <a class="result__url" href="...">
    links = re.findall(r'href="(.*?)"', html)
    
    tiktok_ids = set()
    for link in links:
        # Some are redirect links like //duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.tiktok.com...
        decoded = urllib.parse.unquote(link)
        match = re.search(r'tiktok\.com/@[^/]+/video/(\d+)', decoded)
        if match:
            tiktok_ids.add(match.group(1))

    print(f"FOUND IDs: {tiktok_ids}")
    
    # Try embedding them
    valid = []
    for vid in tiktok_ids:
        oembed_url = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/{vid}"
        try:
            req2 = urllib.request.Request(oembed_url, headers=headers)
            res2 = urllib.request.urlopen(req2).read().decode('utf-8')
            valid.append(vid)
            print(f"VALID: {vid}")
            if len(valid) == 3:
                break
        except Exception as e:
            pass
    print("FINISHED VALID:", valid)

except Exception as e:
    print("Error:", e)
