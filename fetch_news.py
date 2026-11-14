#!/usr/bin/env python3
"""
Pokémon GO 공식 뉴스 스크래퍼
- pokemongolive.com/news 페이지에서 최신 뉴스 10개 추출
- 한국어 번역 (MyMemory Translation API)
- news.json 생성 → GitHub Pages에서 fetch('news.json')로 사용

사용법:
  python3 fetch_news.py
  (GitHub Actions에서 1시간마다 자동 실행)
"""

import re
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone

NEWS_URL = "https://pokemongolive.com/news"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
MAX_NEWS = 10
TRANSLATION_CACHE = "translation_cache.json"


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def load_cache() -> dict:
    """번역 캐시 로드"""
    try:
        with open(TRANSLATION_CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(cache: dict) -> None:
    """번역 캐시 저장"""
    with open(TRANSLATION_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def translate_en_to_ko(text: str) -> str:
    """MyMemory Translation API로 영어→한국어 번역"""
    if not text:
        return ""

    # 캐시 확인
    cache = load_cache()
    if text in cache:
        return cache[text]

    # API 호출
    url = (
        f"https://api.mymemory.translated.net/get?"
        f"q={urllib.parse.quote(text)}&langpair=en|ko"
    )
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated = data.get("responseData", {}).get("translatedText", "")
            if translated:
                cache[text] = translated
                save_cache(cache)
            return translated
    except Exception as e:
        print(f"  [warn] translation failed for '{text[:50]}': {e}", file=sys.stderr)
        return ""


def extract_article_summary(url: str) -> str:
    """뉴스 기사 페이지에서 첫 번째 단락을 요약으로 추출합니다."""
    try:
        html = fetch_html(url)
        # 기사 본문 영역 (_content_) 에서만 <p> 태그 추출
        content_start = html.find("_content_")
        if content_start == -1:
            return ""
        content_area = html[content_start:content_start + 15000]
        # 본문 영역에서 <p> 태그 추출
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_area, re.DOTALL)
        texts = []
        for p in paragraphs:
            text = re.sub(r'<[^>]+>', '', p).strip()
            if text and len(text) > 30:
                texts.append(text)
        # 첫 번째는 제목/날짜일 수 있으니 두 번째(인덱스 1)를 요약으로 사용
        if len(texts) >= 2:
            summary = texts[1]
            return summary[:200] + ("..." if len(summary) > 200 else "")
        elif texts:
            summary = texts[0]
            return summary[:200] + ("..." if len(summary) > 200 else "")
    except Exception as e:
        print(f"  [warn] failed to fetch summary for {url}: {e}", file=sys.stderr)
    return ""


def extract_news_items(html: str) -> list:
    """뉴스 페이지에서 뉴스 항목들을 추출합니다."""
    news = []

    # pokemongolive.com/news 페이지 구조 분석:
    # 뉴스 항목은 <a> 태그로 감싸져 있고 href="/news/..." 패턴을 가짐
    # 제목은 <h3> 또는 <h2> 태그 안에 있음
    # 이미지는 <img> 태그 안에 있고, alt 속성에 제목이 들어있을 수 있음

    # 패턴 1: 뉴스 카드 전체 구조 찾기
    # <a class="..." href="/news/...">...</a> 패턴
    news_blocks = re.findall(
        r'<a[^>]*href=["\'](/news/[^"\']+)[^>]*>(.*?)</a>',
        html,
        re.DOTALL
    )

    if not news_blocks:
        # 패턴 2: 더 넓은 검색 - 뉴스 관련 모든 링크
        news_links = re.findall(
            r'<a[^>]*href=["\'](/news/[^"\']+)[^>]*>',
            html
        )
        for link in news_links:
            news.append({
                "url": f"https://pokemongolive.com{link}",
                "title": "",
                "title_ko": "",
                "summary": "",
                "summary_ko": "",
                "image": "",
                "published": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            })
        return news

    for link, block in news_blocks:
        # 이미지가 없으면 block에서 찾기
        image = ""
        img_match = re.search(
            r'<img[^>]*src=["\']([^"\']+)["\']',
            block, re.DOTALL
        )
        if img_match:
            image = img_match.group(1)

        # 제목 추출 — pokemongolive.com/news에서는 <h> 태그가 아닌 div 텍스트로 제공됨
        # 패턴: <div class="_newsCardTitle_...">제목 텍스트</div>
        title = ""
        title_match = re.search(
            r'class=["\'][^"\']*_newsCardTitle[^"\']*["\']>(.*?)</div>',
            block, re.DOTALL
        )
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

        if title or link:
            news.append({
                "url": f"https://pokemongolive.com{link}",
                "title": title,
                "title_ko": "",
                "summary": "",
                "summary_ko": "",
                "image": image,
                "published": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            })

    return news


def deduplicate(existing: list, new_items: list) -> list:
    """중복 제거 — URL 기준으로 기존에 없는 뉴스만 필터링"""
    existing_urls = {item.get("url", "") for item in existing}
    filtered = []
    for item in new_items:
        url = item.get("url", "")
        if url and url not in existing_urls:
            filtered.append(item)
    return filtered


def translate_news_items(items: list) -> int:
    """새 뉴스 항목들의 제목을 한국어로 번역"""
    translated_count = 0
    for item in items:
        title = item.get("title", "")
        if title and not item.get("title_ko"):
            ko = translate_en_to_ko(title)
            if ko:
                item["title_ko"] = ko
                translated_count += 1
    return translated_count


def extract_summaries(items: list) -> int:
    """새 뉴스 항목들의 기사 본문 요약을 추출합니다."""
    extracted_count = 0
    for item in items:
        url = item.get("url", "")
        if url and not item.get("summary"):
            summary = extract_article_summary(url)
            if summary:
                item["summary"] = summary
                extracted_count += 1
    return extracted_count


def translate_summaries(items: list) -> int:
    """요약 내용을 한국어로 번역합니다."""
    translated_count = 0
    for item in items:
        summary = item.get("summary", "")
        if summary and not item.get("summary_ko"):
            ko = translate_en_to_ko(summary)
            if ko:
                item["summary_ko"] = ko
                translated_count += 1
    return translated_count


def main():
    print("Fetching Pokémon GO news...", file=sys.stderr)
    html = fetch_html(NEWS_URL)
    print(f"Fetched {len(html):,} bytes", file=sys.stderr)

    # 기존 뉴스 로드 (중복 체크용)
    existing = []
    try:
        with open("news.json", "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"Loaded {len(existing)} existing news items", file=sys.stderr)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No existing news.json — starting fresh", file=sys.stderr)

    # 뉴스 추출
    new_items = extract_news_items(html)
    print(f"Extracted {len(new_items)} new items from page", file=sys.stderr)

    # 중복 제거
    unique_new = deduplicate(existing, new_items)
    print(f"{len(unique_new)} unique new news items found", file=sys.stderr)

    # 새 뉴스 항목들의 제목 번역
    if unique_new:
        print(f"Translating {len(unique_new)} new titles to Korean...", file=sys.stderr)
        translate_news_items(unique_new)

    # 새 뉴스 항목들의 본문 요약 추출
    if unique_new:
        print(f"Extracting summaries for {len(unique_new)} new articles...", file=sys.stderr)
        extract_summaries(unique_new)

    # 요약 내용을 한국어로 번역
    if unique_new:
        print(f"Translating {len(unique_new)} summaries to Korean...", file=sys.stderr)
        translate_summaries(unique_new)

    # 기존 뉴스 항목 중 요약이 없는 것들도 처리
    existing_missing_summary = [item for item in existing if not item.get("summary")]
    if existing_missing_summary:
        print(f"Filling summaries for {len(existing_missing_summary)} existing items...", file=sys.stderr)
        extract_summaries(existing_missing_summary)
        translate_summaries(existing_missing_summary)
    all_news = unique_new + existing
    if len(all_news) > MAX_NEWS:
        all_news = all_news[:MAX_NEWS]

    if not all_news:
        print("WARNING: no news extracted", file=sys.stderr)
        # 기존 데이터가 있으면 그대로 유지
        if existing:
            out = json.dumps(existing, indent=2, ensure_ascii=False)
            with open("news.json", "w", encoding="utf-8") as f:
                f.write(out)
                f.write("\n")
            print(f"news.json kept ({len(existing)} items)", file=sys.stderr)
        return

    out = json.dumps(all_news, indent=2, ensure_ascii=False)
    with open("news.json", "w", encoding="utf-8") as f:
        f.write(out)
        f.write("\n")

    print(f"news.json written ({len(all_news)} items):\n{out}", file=sys.stderr)


if __name__ == "__main__":
    main()
