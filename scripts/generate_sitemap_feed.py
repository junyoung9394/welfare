"""
자동으로 sitemap.xml과 feed.xml을 재생성합니다.
GitHub Actions 또는 로컬에서 직접 실행 가능:
  python scripts/generate_sitemap_feed.py
"""

import os
import re
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_URL = "https://welfare.luckygrampus.com"
ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "posts"
KST = timezone(timedelta(hours=9))

# 정적 페이지 (posts 외)
STATIC_PAGES = [
    {"loc": f"{BASE_URL}/", "lastmod": None, "changefreq": "daily", "priority": "1.0"},
    {"loc": f"{BASE_URL}/search.html", "lastmod": None, "changefreq": "weekly", "priority": "0.9"},
    {"loc": f"{BASE_URL}/welfare-calendar.html", "lastmod": None, "changefreq": "weekly", "priority": "0.95"},
    {"loc": f"{BASE_URL}/calculator.html", "lastmod": None, "changefreq": "monthly", "priority": "0.8"},
    {"loc": f"{BASE_URL}/%EC%B2%AD%EB%85%84-%EC%A7%80%EC%9B%90%EA%B8%88.html", "lastmod": None, "changefreq": "weekly", "priority": "0.95"},
    {"loc": f"{BASE_URL}/%EB%85%B8%EC%9D%B8-%EB%B3%B5%EC%A7%80.html", "lastmod": None, "changefreq": "weekly", "priority": "0.95"},
    {"loc": f"{BASE_URL}/%EC%9E%A5%EC%95%A0%EC%9D%B8-%EB%B3%B5%EC%A7%80.html", "lastmod": None, "changefreq": "weekly", "priority": "0.95"},
    {"loc": f"{BASE_URL}/%EC%A7%80%EC%97%AD%EB%B3%84-%EB%B3%B5%EC%A7%80.html", "lastmod": None, "changefreq": "weekly", "priority": "0.95"},
]


def extract_meta(html: str):
    """HTML에서 og:title, description, datePublished 추출"""
    title = ""
    m = re.search(r'property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html)
    if not m:
        m = re.search(r'<title>([^<]+)</title>', html)
    if m:
        title = re.sub(r'\s*[|—–]\s*복지모아.*$', '', m.group(1)).strip()

    desc = ""
    m = re.search(r'name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html)
    if not m:
        m = re.search(r'property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        desc = m.group(1).strip()

    date_str = ""
    m = re.search(r'"datePublished":\s*"([^"]+)"', html)
    if m:
        date_str = m.group(1)[:10]

    return title, desc, date_str


def get_posts():
    """posts/ 폴더의 모든 HTML 파일을 파싱"""
    posts = []
    for f in sorted(POSTS_DIR.iterdir()):
        if not f.suffix == '.html':
            continue
        html = f.read_text(encoding='utf-8')
        title, desc, date_str = extract_meta(html)
        encoded = urllib.parse.quote(f.name, safe='.-')
        posts.append({
            "filename": f.name,
            "loc": f"{BASE_URL}/posts/{encoded}",
            "title": title or f.stem.replace('-', ' '),
            "desc": desc,
            "date": date_str or datetime.now(KST).strftime('%Y-%m-%d'),
        })
    return posts


def build_sitemap(posts):
    today = datetime.now(KST).strftime('%Y-%m-%d')
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             '']

    for page in STATIC_PAGES:
        lastmod = page["lastmod"] or today
        lines += [
            '  <url>',
            f'    <loc>{page["loc"]}</loc>',
            f'    <lastmod>{lastmod}</lastmod>',
            f'    <changefreq>{page["changefreq"]}</changefreq>',
            f'    <priority>{page["priority"]}</priority>',
            '  </url>',
            '',
        ]

    for p in posts:
        lines += [
            '  <url>',
            f'    <loc>{p["loc"]}</loc>',
            f'    <lastmod>{p["date"]}</lastmod>',
            '    <changefreq>monthly</changefreq>',
            '    <priority>0.9</priority>',
            '  </url>',
            '',
        ]

    lines.append('</urlset>')
    return '\n'.join(lines)


def rfc822(date_str: str) -> str:
    """YYYY-MM-DD → RFC 822 형식"""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=KST)
    except Exception:
        dt = datetime.now(KST)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return f"{days[dt.weekday()]}, {dt.day:02d} {months[dt.month-1]} {dt.year} 09:00:00 +0900"


def esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_feed(posts):
    now_rfc = rfc822(datetime.now(KST).strftime('%Y-%m-%d'))

    # 허브 페이지 아이템 (고정)
    hub_items = [
        {
            "loc": f"{BASE_URL}/%EC%B2%AD%EB%85%84-%EC%A7%80%EC%9B%90%EA%B8%88.html",
            "title": "청년 지원금 총정리 2026 — 월세·청약·저축·취업 지원 한눈에",
            "desc": "2026년 만 19~34세 청년이 받을 수 있는 정부 지원금 전체 목록.",
            "date": datetime.now(KST).strftime('%Y-%m-%d'),
        },
        {
            "loc": f"{BASE_URL}/%EB%85%B8%EC%9D%B8-%EB%B3%B5%EC%A7%80.html",
            "title": "노인 복지 총정리 2026 — 기초연금·일자리·장기요양 지원 한눈에",
            "desc": "2026년 만 65세 이상 노인이 받을 수 있는 복지 혜택 전체 목록.",
            "date": datetime.now(KST).strftime('%Y-%m-%d'),
        },
        {
            "loc": f"{BASE_URL}/%EC%9E%A5%EC%95%A0%EC%9D%B8-%EB%B3%B5%EC%A7%80.html",
            "title": "장애인 복지 총정리 2026 — 연금·활동지원·금융 지원 한눈에",
            "desc": "2026년 장애인이 받을 수 있는 복지 혜택 전체 목록.",
            "date": datetime.now(KST).strftime('%Y-%m-%d'),
        },
        {
            "loc": f"{BASE_URL}/%EC%A7%80%EC%97%AD%EB%B3%84-%EB%B3%B5%EC%A7%80.html",
            "title": "지역별 복지 지원금 총정리 2026 — 내 지역 추가 혜택 확인",
            "desc": "2026년 서울·경기·부산 등 지역별 추가 복지 지원금 총정리.",
            "date": datetime.now(KST).strftime('%Y-%m-%d'),
        },
    ]

    # 최신순 정렬 포스트 (최대 40개)
    sorted_posts = sorted(posts, key=lambda p: p['date'], reverse=True)[:40]

    items = []
    for item in hub_items + sorted_posts:
        loc = item.get('loc') or item.get('loc', '')
        items.append(f"""    <item>
      <title>{esc(item['title'])}</title>
      <link>{loc}</link>
      <guid isPermaLink="true">{loc}</guid>
      <description>{esc(item['desc'])}</description>
      <pubDate>{rfc822(item['date'])}</pubDate>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>복지모아 — 정부 지원금·복지혜택 정보</title>
    <link>{BASE_URL}</link>
    <description>2026년 최신 정부 지원금, 복지혜택 정보를 한곳에서 확인하세요.</description>
    <language>ko</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>"""


if __name__ == "__main__":
    posts = get_posts()
    print(f"포스트 {len(posts)}개 발견")

    sitemap = build_sitemap(posts)
    (ROOT / "sitemap.xml").write_text(sitemap, encoding='utf-8')
    ET.parse(ROOT / "sitemap.xml")  # 유효성 검사
    print(f"sitemap.xml 재생성 완료 ({len(posts) + len(STATIC_PAGES)}개 URL)")

    feed = build_feed(posts)
    (ROOT / "feed.xml").write_text(feed, encoding='utf-8')
    ET.parse(ROOT / "feed.xml")
    print("feed.xml 재생성 완료")
