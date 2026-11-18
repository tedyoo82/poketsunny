#!/usr/bin/env python3
"""
Pokémon GO 이벤트 스크래퍼
- pokemongo.com/ko/news 페이지에서 이벤트 관련 뉴스 추출
- 이벤트명, 타입, 날짜, URL 파싱 → events.json 생성
- GitHub Actions에서 15분마다 자동 실행

이벤트 타입:
  community    - 커뮤니티 데이
  raid         - 레이드 데이 / 슈퍼 메가 레이드
  hatch        - 부화데이
  season       - 시즌
  maxbattle    - 맥스배틀 데이
  wildweek     - 와일드 위크
  research     - 리서치
  store        - 스토어 세일 / 특별 박스
  collab       - 협업 이벤트 (아디다스 등)
  special      - 기타 특별 이벤트
"""

import re
import json
import html as html_util
import sys
import urllib.request
from datetime import datetime, timezone

NEWS_URL = "https://pokemongo.com/ko/news"
EVENTS_URL = "https://pokemongo.com/ko/events"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
MAX_EVENTS = 10

# 이벤트 키워드 매핑 (한국어)
EVENT_KEYWORDS = {
    "community": ["커뮤니티 데이", "커뮤데이", "community day"],
    "raid": ["레이드 데이", "레이드데이", "raid day"],
    "supermega": ["슈퍼 메가 레이드", "슈퍼메가", "super mega raid"],
    "hatch": ["부화데이", "부화 데이", "hatch day"],
    "maxbattle": ["맥스배틀", "맥스배틀 데이", "max battle"],
    "wildweek": ["와일드 위크", "wild week"],
    "research": ["리서치", "레서치", "research"],
    "store": ["스토어", "포켓코인", "스페셜 박스", "세일"],
    "season": ["시즌", "season"],
    "collab": ["아디다스", "크록스", "collab", "컬렉션"],
    "special": [
        "스페셜", "스페셜 이벤트", "스페셜 리서치",
        "스페셜 리서치 미션", "special",
    ],
    "wildarea": ["와일드 에리어", "wild area"],
    "go": ["GO패스", "go pass", "go pass:"],
}

# 날짜 패턴 (한국어 형식)
DATE_PATTERNS = [
    r"(\d{4}년\s*\d{1,2}월\s*\d{1,2}일)",           # 2026년 12월 5일
    r"(\d{1,2}월\s*\d{1,2}일)",                       # 12월 5일
    r"(\d{1,2}\/\d{1,2})",                            # 12/05
    r"(\d{4}\.\d{1,2}\.\d{1,2})",                     # 2026.12.05
    r"(\d{4}-\d{1,2}-\d{1,2})",                       # 2026-12-05
]


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def classify_event(title: str, summary: str, content: str) -> str:
    """제목/내용에서 이벤트 타입 분류"""
    text = f"{title} {summary} {content}".lower()
    for event_type, keywords in EVENT_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                return event_type
    return "special"


def parse_dates(text: str) -> list:
    """텍스트에서 날짜 추출"""
    dates = []
    for pattern in DATE_PATTERNS:
        matches = re.findall(pattern, text)
        for m in matches:
            dates.append(m.strip())
    return list(dict.fromkeys(dates))  # 중복 제거 + 순서 유지


def normalize_date(date_str: str) -> str:
    """날짜를 YYYY-MM-DD 형식으로 정규화"""
    # 2026년 12월 5일 → 2026-12-05
    m = re.match(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", date_str)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # 12월 5일 → 현재년+YYYY-MM-DD
    m = re.match(r"(\d{1,2})월\s*(\d{1,2})일", date_str)
    if m:
        year = datetime.now().year
        return f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"

    # 12/05 → YYYY/MM/DD
    m = re.match(r"(\d{1,2})/(\d{1,2})", date_str)
    if m:
        year = datetime.now().year
        return f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"

    # 2026.12.05
    m = re.match(r"(\d{4})\.(\d{1,2})\.(\d{1,2})", date_str)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    # 2026-12-05 (이미 올바른 형식)
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_str)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    return date_str


def extract_event_info(html: str, url: str) -> dict:
    """뉴스 기사에서 이벤트 정보 추출"""
    try:
        content = fetch_html(url)
    except Exception as e:
        print(f"  [warn] failed to fetch body: {e}", file=sys.stderr)
        return {}

    # 텍스트 추출
    text = re.sub(r'<[^>]+>', ' ', content)
    text = html_util.unescape(text)

    # 제목 추출
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    title = ""
    if title_match:
        title = html_util.unescape(re.sub(r'<[^>]+>', '', title_match.group(1)).strip())

    # 요약 추출
    summary = ""
    para_matches = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    for p in para_matches:
        t = html_util.unescape(re.sub(r'<[^>]+>', '', p).strip())
        if t and len(t) > 30:
            summary = t[:300]
            break

    # 이벤트 타입 분류
    event_type = classify_event(title, summary, text)

    # 날짜 추출
    raw_dates = parse_dates(f"{title} {summary} {text}")
    dates = []
    for d in raw_dates[:3]:  # 최대 3개 날짜
        normalized = normalize_date(d)
        if normalized and not normalized.startswith("00"):
            dates.append(normalized)

    # 이미지 추출
    image = ""
    img_match = re.search(r'<img[^>]*src=["\']([^"\']+)["\']', content)
    if img_match:
        image = img_match.group(1)

    # 이벤트명 정리
    event_name = title
    if not event_name:
        event_name = summary[:50] + "..." if summary else "이벤트"

    return {
        "url": url,
        "name": event_name,
        "type": event_type,
        "dates": dates,
        "summary": summary[:200] if summary else "",
        "image": image,
    }


def extract_news_items(html: str) -> list:
    """뉴스 페이지에서 뉴스 링크 추출"""
    news = []
    blocks = re.findall(
        r'<a[^>]+href=["\'](/ko/news/[^"\']+)[^>]*>(.*?)</a>',
        html, re.DOTALL
    )
    if not blocks:
        links = re.findall(r'<a[^>]*href=["\'](/ko/news/[^"\']+)[^>]*>', html)
        for link in links:
            news.append(f"https://pokemongo.com{link}")
        return news

    for link, block in blocks:
        url = f"https://pokemongo.com{link}"
        # 이미지 확인 (이벤트 관련일 가능성)
        img_match = re.search(r'<img[^>]*src=["\']([^"\']+)["\']', block, re.DOTALL)
        news.append({
            "url": url,
            "has_image": bool(img_match),
        })
    return news


def is_event_article(item: dict, title: str = "", content: str = "") -> bool:
    """뉴스 기사가 이벤트 관련인지 판단"""
    url = item["url"]
    text = f"{url} {title} {content}".lower()

    # URL에 이벤트 키워드가 있으면 이벤트 관련
    event_patterns = [
        "community", "raid", "season", "event", "special",
        "패스", "세일", "sale", "박스", "collection",
        "맥스배틀", "부화", "슈퍼메가",
    ]
    for pat in event_patterns:
        if pat in text:
            return True
    return False


def main():
    print("Fetching Pokémon GO events from news...", file=sys.stderr)

    # 기존 이벤트 로드
    existing = []
    try:
        with open("events.json", "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"Loaded {len(existing)} existing events", file=sys.stderr)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No existing events.json — starting fresh", file=sys.stderr)

    # 뉴스 페이지에서 기사 링크 추출
    html = fetch_html(NEWS_URL)
    items = extract_news_items(html)
    print(f"Found {len(items)} news items", file=sys.stderr)

    # 이벤트 관련 기사 필터링 + 정보 추출
    events = []
    for item in items:
        url = item["url"]
        # 기존 이벤트와 중복 체크
        if any(e["url"] == url for e in existing):
            continue
        if len(events) >= MAX_EVENTS:
            break

        info = extract_event_info(html, url)
        if info.get("name") and (info.get("dates") or info.get("type") != "special"):
            events.append(info)
            print(f"  Found: {info['name']} [{info['type']}] dates={info['dates']}", file=sys.stderr)

    # 기존 이벤트 + 신규 이벤트 (신규가 우선)
    all_events = events + existing
    if len(all_events) > MAX_EVENTS:
        all_events = all_events[:MAX_EVENTS]

    if not all_events:
        print("WARNING: no events extracted, keeping existing data", file=sys.stderr)
        if existing:
            out = json.dumps(existing, indent=2, ensure_ascii=False)
            with open("events.json", "w", encoding="utf-8") as f:
                f.write(out)
                f.write("\n")
            print(f"events.json kept ({len(existing)} items)", file=sys.stderr)
        return

    out = json.dumps(all_events, indent=2, ensure_ascii=False)
    with open("events.json", "w", encoding="utf-8") as f:
        f.write(out)
        f.write("\n")

    print(f"events.json written ({len(all_events)} items)", file=sys.stderr)


if __name__ == "__main__":
    main()
