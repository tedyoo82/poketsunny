#!/usr/bin/env python3
"""
포케써니 YouTube 채널 최근 영상 스크래퍼
- YouTube 채널 /videos 페이지 HTML에서 ytInitialData 추출
- 최근 6개 영상 → recent_videos.json

사용법:
  python3 fetch_videos.py
  (GitHub Actions에서 매일 자동 실행)
"""

import re
import json
import sys
import urllib.request

VIDEOS_URL = "https://www.youtube.com/@Poke_Sunny/videos"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
MAX_VIDEOS = 6


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def clean_title(raw: str) -> str:
    """'11.[포켓몬GO] 잠들기 전...' → '잠들기 전...' (번호·채널명 제거)"""
    t = raw
    # leading number + dot
    t = re.sub(r'^\d+\.\s*', '', t)
    # [포켓몬GO] prefix
    t = re.sub(r'^\[포켓몬GO\]\s*', '', t)
    return t.strip()


def extract_yt_initial_data(html: str):
    m = re.search(r'var ytInitialData\s*=\s*({.*?});\s*</script>', html, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    m = re.search(r'ytInitialData\s*=\s*({.*?});\s*</script>', html, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    return None


def main():
    print("Fetching /videos page...", file=sys.stderr)
    html = fetch_html(VIDEOS_URL)
    print(f"Fetched {len(html):,} bytes", file=sys.stderr)

    data = extract_yt_initial_data(html)
    if not data:
        print("ERROR: ytInitialData not found", file=sys.stderr)
        sys.exit(1)

    # Navigate: contents → twoColumnBrowseResultsRenderer → tabs[0] → tabRenderer → content → richGridRenderer
    try:
        tcbr = data["contents"]["twoColumnBrowseResultsRenderer"]
        tab0 = tcbr["tabs"][0]["tabRenderer"]
        rich = tab0["content"]["richGridRenderer"]
    except (KeyError, IndexError, TypeError) as e:
        print(f"ERROR: unexpected structure: {e}", file=sys.stderr)
        sys.exit(1)

    videos = []
    for item in rich.get("contents", []):
        if "richItemRenderer" not in item:
            continue
        content = item["richItemRenderer"].get("content", {})
        if "lockupViewModel" not in content:
            continue
        lm = content["lockupViewModel"]

        vid = lm.get("contentId", "")
        if not vid:
            continue

        # Title
        md = lm.get("metadata", {}).get("lockupMetadataViewModel", {})
        raw_title = md.get("title", {}).get("content", "")
        title = clean_title(raw_title)

        # Metadata: views + published
        views = ""
        published = ""
        rows = md.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
        for row in rows:
            for part in row.get("metadataParts", []):
                t = part.get("text", {}).get("content", "")
                if not t:
                    continue
                # "113" or "1,234" → views (digits only)
                if re.match(r'^[\d,]+$', t):
                    views = t
                elif "전" in t or "개월" in t or "년" in t:
                    published = t

        # Duration
        duration = ""
        for ov in lm.get("contentImage", {}).get("thumbnailViewModel", {}).get("overlays", []):
            for b in ov.get("thumbnailBottomOverlayViewModel", {}).get("badges", []):
                t = b.get("thumbnailBadgeViewModel", {}).get("text", "")
                if re.match(r'^\d+:\d+', t):
                    duration = t
                    break
            if duration:
                break

        # Thumbnail — use clean i.ytimg.com URL (strip query params)
        thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"

        videos.append({
            "id": vid,
            "title": title,
            "views": views,
            "published": published,
            "duration": duration,
            "thumb": thumb,
        })

        if len(videos) >= MAX_VIDEOS:
            break

    if not videos:
        print("ERROR: no videos extracted", file=sys.stderr)
        sys.exit(1)

    out = json.dumps(videos, indent=2, ensure_ascii=False)
    with open("recent_videos.json", "w", encoding="utf-8") as f:
        f.write(out)
        f.write("\n")

    print(f"recent_videos.json written ({len(videos)} videos):\n{out}", file=sys.stderr)


if __name__ == "__main__":
    main()
