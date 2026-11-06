#!/usr/bin/env python3
"""
포케써니 YouTube 채널 통계 스크래퍼
- YouTube 채널 페이지 HTML에서 subscriberCountText / videoCountText / viewCountText 추출
- stats.json 생성 → GitHub Pages에서 fetch('stats.json')로 사용

사용법:
  python3 fetch_stats.py
  (GitHub Actions에서 매일 자동 실행)
"""

import re
import json
import sys
import urllib.request
from datetime import datetime, timezone

CHANNEL_URL = "https://www.youtube.com/@Poke_Sunny/about"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_num(text: str) -> int:
    """'구독자 114명' / '153,532' / '66' → 114 / 153532 / 66"""
    if not text:
        return 0
    m = re.search(r"(\d[\d,\.]*)", text)
    if not m:
        return 0
    return int(m.group(1).replace(",", "").replace(".", ""))


def extract(html: str, pattern: str) -> str:
    m = re.search(pattern, html, re.IGNORECASE)
    return m.group(1) if m else None


def main():
    print("Fetching channel page...", file=sys.stderr)
    html = fetch_html(CHANNEL_URL)
    print(f"Fetched {len(html):,} bytes", file=sys.stderr)

    sub_raw = extract(html, r'"subscriberCountText"\s*:\s*"([^"]+)"')
    video_raw = extract(html, r'"videoCountText"\s*:\s*"([^"]+)"')
    view_raw = extract(html, r'"viewCountText"\s*:\s*"([^"]+)"')

    print(f"subscriberCountText: {sub_raw}", file=sys.stderr)
    print(f"videoCountText:      {video_raw}", file=sys.stderr)
    print(f"viewCountText:       {view_raw}", file=sys.stderr)

    stats = {
        "subscribers": parse_num(sub_raw),
        "videos": parse_num(video_raw),
        "views": parse_num(view_raw),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # 0이면 파싱 실패 — 예전 값 유지
    if stats["subscribers"] == 0 and stats["videos"] == 0:
        print("ERROR: failed to extract stats", file=sys.stderr)
        sys.exit(1)

    out = json.dumps(stats, indent=2, ensure_ascii=False)
    with open("stats.json", "w", encoding="utf-8") as f:
        f.write(out)
        f.write("\n")

    print(f"stats.json written:\n{out}", file=sys.stderr)


if __name__ == "__main__":
    main()
