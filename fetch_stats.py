#!/usr/bin/env python3
"""
포케써니 YouTube 채널 통계 스크래퍼
- YouTube Data API v3를 통해 subscriberCount / videoCount / viewCount 추출
- stats.json 생성 → GitHub Pages에서 fetch('stats.json')로 사용

사용법:
  python3 fetch_stats.py
  (GitHub Actions에서 15분마다 자동 실행)
"""

import json
import sys
import urllib.request
from datetime import datetime, timezone

API_KEY = "AIzaSyB_H4QQay9aXrXAfvjlt3Aodw0jBx6-K9M"
CHANNEL_ID = "UCf5ymFUkRYToCRFqeYmgsFg"  # Poke_Sunny
API_URL = (
    "https://www.googleapis.com/youtube/v3/channels"
    "?part=statistics"
    f"&id={CHANNEL_ID}"
    f"&key={API_KEY}"
)


def main():
    print("Fetching YouTube stats via API v3...", file=sys.stderr)

    req = urllib.request.Request(API_URL, headers={
        "User-Agent": "PoketSunny-Stats/1.0",
        "Referer": "https://pokesunny.com/",
    })

    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if not data.get("items") or not data["items"]:
        print("ERROR: No channel data found", file=sys.stderr)
        sys.exit(1)

    stats = data["items"][0].get("statistics", {})

    subscribers = int(stats.get("subscriberCount", 0))
    videos = int(stats.get("videoCount", 0))
    views = int(stats.get("viewCount", 0))

    print(f"  Subscribers: {subscribers:,}", file=sys.stderr)
    print(f"  Videos:      {videos:,}", file=sys.stderr)
    print(f"  Views:       {views:,}", file=sys.stderr)

    result = {
        "subscribers": subscribers,
        "videos": videos,
        "views": views,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    out = json.dumps(result, indent=2, ensure_ascii=False)
    with open("stats.json", "w", encoding="utf-8") as f:
        f.write(out)
        f.write("\n")

    print(f"stats.json written:\n{out}", file=sys.stderr)


if __name__ == "__main__":
    main()
