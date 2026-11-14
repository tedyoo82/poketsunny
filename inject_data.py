#!/usr/bin/env python3
"""stats.json, recent_videos.json, news.json의 데이터를 index.html에 임베드."""
import json
import re
import sys


def main():
    # JSON 파일 읽기
    try:
        with open("stats.json", "r", encoding="utf-8") as f:
            stats = json.load(f)
    except Exception as e:
        print(f"stats.json 읽기 실패: {e}", file=sys.stderr)
        stats = {"subscribers": 0, "videos": 0, "views": 0}

    try:
        with open("recent_videos.json", "r", encoding="utf-8") as f:
            videos = json.load(f)
    except Exception as e:
        print(f"recent_videos.json 읽기 실패: {e}", file=sys.stderr)
        videos = []

    try:
        with open("news.json", "r", encoding="utf-8") as f:
            news = json.load(f)
    except Exception as e:
        print(f"news.json 읽기 실패: {e}", file=sys.stderr)
        news = []

    # HTML 읽기
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # JSON 데이터를 문자열로 직렬화
    stats_js = json.dumps(stats, ensure_ascii=False)
    videos_js = json.dumps(videos, ensure_ascii=False)
    news_js = json.dumps(news, ensure_ascii=False)

    # inline-data script 태그 교체 (있으면) 또는 삽입 (없으면)
    inline_block = (
        f'<script id="inline-data" type="application/json">{stats_js}</script>\n'
        f'<script id="inline-videos" type="application/json">{videos_js}</script>\n'
        f'<script id="inline-news" type="application/json">{news_js}</script>\n'
    )

    if '<script id="inline-data"' in html:
        # 기존 inline-data ~ /script> 블록을 교체
        html = re.sub(
            r'<script id="inline-data".*?</script>\s*'
            r'<script id="inline-videos".*?</script>\s*'
            r'<script id="inline-news".*?</script>',
            inline_block.strip(),
            html,
            flags=re.DOTALL,
        )
    else:
        # Firebase script 직전에 삽입
        html = html.replace(
            '<script src="https://www.gstatic.com/firebasejs/',
            inline_block
            + '  <script src="https://www.gstatic.com/firebasejs/',
        )

    # data-count attributes 업데이트 (히어로 통계)
    # 구독자 (첫 번째 stat__num)
    if "subscribers" in stats and stats["subscribers"]:
        html = re.sub(
            r'(class="stat__num" data-count=")\d+(\s*>)',
            lambda m: m.group(1) + str(stats["subscribers"]) + m.group(2),
            html,
            count=1,
        )
    # 동영상 (두 번째 stat__num)
    if "videos" in stats and stats["videos"]:
        matches = list(
            re.finditer(r'(class="stat__num" data-count=")\d+(\s*>)', html)
        )
        if len(matches) >= 2:
            m = matches[1]
            html = (
                html[: m.start(1)]
                + m.group(1)
                + str(stats["videos"])
                + m.group(2)
                + html[m.end(2) :]
            )
    # 조회수 (세 번째 stat__num)
    if "views" in stats and stats["views"]:
        matches = list(
            re.finditer(r'(class="stat__num" data-count=")\d+(\s*>)', html)
        )
        if len(matches) >= 3:
            m = matches[2]
            html = (
                html[: m.start(1)]
                + m.group(1)
                + str(stats["views"])
                + m.group(2)
                + html[m.end(2) :]
            )

    # HTML 쓰기
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(
        f"✅ HTML 업데이트: 구독자={stats.get('subscribers', '?')}, "
        f"영상={stats.get('videos', '?')}, 조회수={stats.get('views', '?')}"
    )
    print(f"   영상 {len(videos)}개, 뉴스 {len(news)}개 임베드")


if __name__ == "__main__":
    main()
