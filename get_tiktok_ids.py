import urllib.request
import re
import json

url = 'https://www.tiktok.com/@tiktok'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # find json state
    ids = re.findall(r'"id":"(\d{19})"', html)
    
    unique_ids = list(set(ids))
    print("FOUND TIKTOK IDs:", unique_ids[:5])
except Exception as e:
    print("Error:", e)
