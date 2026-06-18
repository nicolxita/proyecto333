import urllib.request
import urllib.parse
import json

# Instead of duckduckgo html, let's use the TikTok Oembed API to verify if an ID works!
# https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/ID
# If it returns JSON with html, it works and is embeddable.

test_ids = [
    '7294819402111394851',
    '7162235921868311854',
    '7181077755839204613',
    '7311111111111111111',
    '7271424911765720362', # A known viral humidifier video
    '7286167886475431210', # Another
    '7326880000000000000'
]

for vid in test_ids:
    url = f"https://www.tiktok.com/oembed?url=https://www.tiktok.com/@user/video/{vid}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        print(f"WORKS: {vid} - Title: {data.get('title')}")
    except Exception as e:
        print(f"FAILED: {vid} - {e}")
