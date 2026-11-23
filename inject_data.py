#!/usr/bin/env python3
"""stats.json, recent_videos.json, news.json, events.json의 데이터를 index.html에 임베드."""
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

    try:
        with open("events.json", "r", encoding="utf-8") as f:
            events = json.load(f)
    except Exception as e:
        print(f"events.json 읽기 실패: {e}", file=sys.stderr)
        events = []

    # HTML 읽기
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # JSON 데이터를 문자열로 직렬화
    stats_js = json.dumps(stats, ensure_ascii=False)
    videos_js = json.dumps(videos, ensure_ascii=False)
    news_js = json.dumps(news, ensure_ascii=False)
    events_js = json.dumps(events, ensure_ascii=False)

    # inline-data script 태그 교체 (있으면) 또는 삽입 (없으면)
    inline_block = (
        f'<script id="inline-data" type="application/json">{stats_js}</script>\n'
        f'<script id="inline-videos" type="application/json">{videos_js}</script>\n'
        f'<script id="inline-news" type="application/json">{news_js}</script>\n'
        f'<script id="inline-events" type="application/json">{events_js}</script>\n'
    )

    # 기존 inline 블록 모두 제거 (중복 방지)
    html = re.sub(
        r'<script id="inline-data"[^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<script id="inline-videos"[^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<script id="inline-news"[^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<script id="inline-events"[^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.DOTALL,
    )

    # Firebase script 직전에 새 데이터 삽입 (첫 번째 위치에만)
    html = html.replace(
        '<script src="https://www.gstatic.com/firebasejs/',
        inline_block
        + '  <script src="https://www.gstatic.com/firebasejs/',
        1,
    )

    # data-count attributes 업데이트 (히어로 통계)
    def set_data_count(index, value):
        nonlocal html
        pattern = r'(class="stat__num" data-count=")\d+(">)'
        matches = list(re.finditer(pattern, html))
        if len(matches) > index:
            m = matches[index]
            html = (
                html[: m.start(1)]
                + m.group(1)
                + str(value)
                + m.group(2)
                + html[m.end(2) :]
            )

    if "subscribers" in stats and stats["subscribers"]:
        set_data_count(0, stats["subscribers"])
    if "videos" in stats and stats["videos"]:
        set_data_count(1, stats["videos"])
    if "views" in stats and stats["views"]:
        set_data_count(2, stats["views"])

    # stat__val 초기 표시 숫자 업데이트 (애니메이션 시작 값)
    val_idx = [0]
    new_vals = [
        str(stats.get("subscribers", "")),
        str(stats.get("videos", "")),
        f"{stats.get('views', 0):,}",
    ]

    def replace_val(m):
        if val_idx[0] < len(new_vals):
            result = f'<span class="stat__val">{new_vals[val_idx[0]]}</span>'
            val_idx[0] += 1
            return result
        return m.group(0)

    html = re.sub(r"<span class=\"stat__val\">[^<]*</span>", replace_val, html, count=3)

    # HTML 쓰기
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(
        f"✅ HTML 업데이트: 구독자={stats.get('subscribers', '?')}, "
        f"영상={stats.get('videos', '?')}, 조회수={stats.get('views', '?')}"
    )
    print(f"   영상 {len(videos)}개, 뉴스 {len(news)}개, 이벤트 {len(events)}개 임베드")


if __name__ == "__main__":
    main()
