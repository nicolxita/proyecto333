import urllib.request
import json

test_ids = [
    '6718335390845095173', # Official docs example
    '7105260172355554566',
    '7201880482592034050'
]

valid = []
for vid in test_ids:
    url = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/{vid}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        valid.append(vid)
        print(f"WORKS: {vid} - Title: {data.get('title')}")
    except Exception as e:
        print(f"FAILED: {vid} - {e}")
