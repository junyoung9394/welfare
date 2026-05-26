"""
사이트 상태를 점검하고 리포트를 출력합니다.
로컬 파일 기반으로 점검 (네트워크 불필요):
  - 포스트 수 / datePublished 누락
  - sitemap.xml URL 수 / 유효성
  - feed.xml 아이템 수 / 유효성
  - 허브 페이지 존재 여부
  - 각 포스트의 og:title, meta description 존재 여부
"""

import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "posts"
KST = timezone(timedelta(hours=9))

HUB_PAGES = [
    "청년-지원금.html", "노인-복지.html", "장애인-복지.html", "지역별-복지.html",
    "기초생활수급.html", "가족-출산-지원.html", "취업-교육-지원.html",
]

issues = []
today = datetime.now(KST).strftime("%Y-%m-%d")

print(f"=== 복지모아 사이트 상태 점검 ({today}) ===\n")

# 1. 포스트 수
posts = list(POSTS_DIR.glob("*.html"))
print(f"✅ 총 포스트 수: {len(posts)}개")

# 2. datePublished 누락
missing_date = []
for p in posts:
    html = p.read_text(encoding="utf-8")
    if '"datePublished"' not in html:
        missing_date.append(p.name)
if missing_date:
    issues.append(f"datePublished 누락 {len(missing_date)}개")
    print(f"⚠️  datePublished 누락: {', '.join(missing_date)}")
else:
    print(f"✅ 모든 포스트에 datePublished 있음")

# 3. og:title / meta description 누락
missing_meta = []
for p in posts:
    html = p.read_text(encoding="utf-8")
    if 'og:title' not in html or 'name="description"' not in html:
        missing_meta.append(p.name)
if missing_meta:
    issues.append(f"og:title/description 누락 {len(missing_meta)}개")
    print(f"⚠️  메타 누락: {', '.join(missing_meta)}")
else:
    print(f"✅ 모든 포스트 og:title/description 있음")

# 4. sitemap.xml
sitemap_path = ROOT / "sitemap.xml"
if sitemap_path.exists():
    try:
        tree = ET.parse(sitemap_path)
        urls = tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        print(f"✅ sitemap.xml: {len(urls)}개 URL, XML 유효")
    except Exception as e:
        issues.append(f"sitemap.xml 오류: {e}")
        print(f"❌ sitemap.xml 오류: {e}")
else:
    issues.append("sitemap.xml 없음")
    print(f"❌ sitemap.xml 없음")

# 5. feed.xml
feed_path = ROOT / "feed.xml"
if feed_path.exists():
    try:
        tree = ET.parse(feed_path)
        items = tree.findall(".//item")
        print(f"✅ feed.xml: {len(items)}개 아이템, XML 유효")
    except Exception as e:
        issues.append(f"feed.xml 오류: {e}")
        print(f"❌ feed.xml 오류: {e}")
else:
    issues.append("feed.xml 없음")
    print(f"❌ feed.xml 없음")

# 6. 허브 페이지
missing_hub = [h for h in HUB_PAGES if not (ROOT / h).exists()]
if missing_hub:
    issues.append(f"허브 페이지 누락: {missing_hub}")
    print(f"❌ 허브 페이지 누락: {missing_hub}")
else:
    print(f"✅ 허브 페이지 7개 모두 존재")

# 최종
print(f"\n{'='*40}")
if issues:
    print(f"⚠️  발견된 이슈 {len(issues)}개:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
    sys.exit(1)
else:
    print(f"✅ 모든 항목 정상")
