#!/usr/bin/env python3
"""
Pokemon GO 코리아 공식 뉴스 스크래퍼
- pokemongo.com/ko/news 페이지에서 최신 뉴스 6개 추출
- 한국어 뉴스 (번역 불필요)
- news.json 생성 -> GitHub Pages에서 fetch('news.json')로 사용

사용법:
  python3 fetch_news.py
  (GitHub Actions에서 15분마다 자동 실행)
"""

import re
import json
import html as html_util
import sys
import urllib.request
from datetime import datetime, timezone

NEWS_URL = "https://pokemongo.com/ko/news"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
MAX_NEWS = 6


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def extract_article_body(url: str) -> str:
    """뉴스 기사 페이지에서 전체 본문(text blocks)을 추출합니다."""
    try:
        html = fetch_html(url)
        content_start = html.find("_content_")
        if content_start == -1:
            return ""
        content_area = html[content_start:content_start + 30000]
        # <p> 태그에서 텍스트 추출
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_area, re.DOTALL)
        texts = []
        for p in paragraphs:
            text = html_util.unescape(re.sub(r'<[^>]+>', '', p).strip())
            if text and len(text) > 15:
                texts.append(text)
        # 본문은 첫 20개 단락까지 (footer 제외)
        body_texts = texts[:20]
        return "\n\n".join(body_texts)
    except Exception as e:
        print(f"  [warn] failed to fetch body for {url}: {e}", file=sys.stderr)
    return ""


def extract_article_summary(url: str) -> str:
    """뉴스 기사 페이지에서 첫 번째 단락을 요약으로 추출합니다."""
    try:
        html = fetch_html(url)
        content_start = html.find("_content_")
        if content_start == -1:
            return ""
        content_area = html[content_start:content_start + 15000]
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_area, re.DOTALL)
        texts = []
        for p in paragraphs:
            text = html_util.unescape(re.sub(r'<[^>]+>', '', p).strip())
            if text and len(text) > 30:
                texts.append(text)
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

    # pokemongo.com/ko/news 페이지 구조:
    # 뉴스 항목은 <a> 태그로 감싸져 있고 href="/ko/news/..." 패턴을 가짐
    news_blocks = re.findall(
        r'<a[^>]+href=["\'](/ko/news/[^"\']+)[^>]*>(.*?)</a>',
        html,
        re.DOTALL
    )

    if not news_blocks:
        # 패턴 2: 더 넓은 검색
        news_links = re.findall(
            r'<a[^>]*href=["\'](/ko/news/[^"\']+)[^>]*>',
            html
        )
        for link in news_links:
            news.append({
                "url": f"https://pokemongo.com{link}",
                "title": "",
                "summary": "",
                "image": "",
                "published": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            })
        return news

    for link, block in news_blocks:
        # 이미지 추출
        image = ""
        img_match = re.search(
            r'<img[^>]*src=["\']([^"\']+)["\']',
            block, re.DOTALL
        )
        if img_match:
            image = img_match.group(1)

        # 제목 추출
        title = ""
        title_match = re.search(
            r'class=["\'][^"\']*_newsCardTitle[^"\']*["\']>(.*?)</div>',
            block, re.DOTALL
        )
        if title_match:
            title = html_util.unescape(re.sub(r'<[^>]+>', '', title_match.group(1)).strip())

        if title or link:
            news.append({
                "url": f"https://pokemongo.com{link}",
                "title": title,
                "summary": "",
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


def extract_bodies(items: list) -> int:
    """새 뉴스 항목들의 기사 본문 전체를 추출합니다."""
    extracted_count = 0
    for item in items:
        url = item.get("url", "")
        if url and not item.get("content"):
            body = extract_article_body(url)
            if body:
                item["content"] = body
                extracted_count += 1
    return extracted_count


def main():
    print("Fetching Pokemon GO Korea news...", file=sys.stderr)
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
    print(f"Extracted {len(new_items)} items from page", file=sys.stderr)

    # 중복 제거
    unique_new = deduplicate(existing, new_items)
    print(f"{len(unique_new)} unique new news items found", file=sys.stderr)

    # 새 뉴스 항목들의 본문 요약 추출
    if unique_new:
        print(f"Extracting summaries for {len(unique_new)} new articles...", file=sys.stderr)
        extract_summaries(unique_new)

    # 새 뉴스 항목들의 본문 전체 추출
    if unique_new:
        print(f"Extracting full body for {len(unique_new)} new articles...", file=sys.stderr)
        extract_bodies(unique_new)

    # 기존 뉴스 항목 중 요약이 없는 것들도 처리
    existing_missing_summary = [item for item in existing if not item.get("summary")]
    if existing_missing_summary:
        print(f"Filling summaries for {len(existing_missing_summary)} existing items...", file=sys.stderr)
        extract_summaries(existing_missing_summary)

    # 기존 뉴스 항목 중 본문이 없는 것들도 처리
    existing_missing_body = [item for item in existing if not item.get("content")]
    if existing_missing_body:
        print(f"Filling full body for {len(existing_missing_body)} existing items...", file=sys.stderr)
        extract_bodies(existing_missing_body)

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

    print(f"news.json written ({len(all_news)} items)", file=sys.stderr)


if __name__ == "__main__":
    main()
