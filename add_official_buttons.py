#!/usr/bin/env python3
import os, re

POSTS = "/home/user/welfare/posts"

# 공식 사이트 라벨 매핑
LABEL_MAP = {
    "work.go.kr":    ("고용24", "https://www.work.go.kr"),
    "nhis.or.kr":    ("국민건강보험공단", "https://www.nhis.or.kr"),
    "nps.or.kr":     ("국민연금공단", "https://www.nps.or.kr"),
    "myhome.go.kr":  ("마이홈포털", "https://www.myhome.go.kr"),
    "kosaf.go.kr":   ("한국장학재단", "https://www.kosaf.go.kr"),
    "hometax.go.kr": ("홈택스", "https://www.hometax.go.kr"),
    "kpass.co.kr":   ("케이패스", "https://www.kpass.co.kr"),
    "bokjiro.go.kr": ("복지로", "https://www.bokjiro.go.kr"),
}

def get_official(html):
    """footer disclaimer에서 공식 URL 추출"""
    m = re.search(
        r'정확한 지원 금액·자격·신청 기간은 <a href="([^"]+)"[^>]*>([^<]+)</a>',
        html
    )
    if m:
        url = m.group(1).strip()
        for domain, (label, _) in LABEL_MAP.items():
            if domain in url:
                return url, label
        return url, m.group(2).strip()
    # 신규 포스트 footer 패턴
    m2 = re.search(r'<a href="([^"]+)" target="_blank" rel="noopener" style="color:var\(--primary\)\.">', html)
    if m2:
        url = m2.group(1).strip()
        for domain, (label, _) in LABEL_MAP.items():
            if domain in url:
                return url, label
    return "https://www.bokjiro.go.kr", "복지로"

def make_top_btn(url, label):
    return (
        f'\n  <div style="margin:0 0 28px;text-align:center;">\n'
        f'    <a href="{url}" target="_blank" rel="noopener"\n'
        f'       style="display:inline-flex;align-items:center;gap:8px;'
        f'background:#1a6fc4;color:#fff;padding:13px 28px;border-radius:10px;'
        f'text-decoration:none;font-weight:700;font-size:0.97rem;'
        f'box-shadow:0 3px 10px rgba(26,111,196,0.28);transition:background 0.2s;">\n'
        f'      🔗 상세 내용은 {label} 홈페이지에서 확인하기 →\n'
        f'    </a>\n'
        f'    <p style="font-size:0.76rem;color:#aaa;margin:7px 0 0;">'
        f'공식 사이트에서 최신 지원 금액 및 신청 기간을 꼭 확인하세요</p>\n'
        f'  </div>\n'
    )

def make_bottom_btn(url, label):
    return (
        f'\n  <div style="background:#f0f7ff;border:1.5px solid #b8d8f8;'
        f'border-radius:12px;padding:18px 20px;margin:28px 0 16px;text-align:center;">\n'
        f'    <p style="margin:0 0 10px;font-size:0.9rem;color:#444;font-weight:600;">'
        f'📋 지원 자격·신청 기간은 공식 사이트에서 확인하세요</p>\n'
        f'    <a href="{url}" target="_blank" rel="noopener"\n'
        f'       style="display:inline-block;background:#1a6fc4;color:#fff;'
        f'padding:11px 26px;border-radius:8px;text-decoration:none;'
        f'font-weight:700;font-size:0.93rem;">\n'
        f'      🏛️ {label} 공식 사이트 바로가기\n'
        f'    </a>\n'
        f'  </div>\n'
    )

updated = 0
skipped = 0

for fname in sorted(os.listdir(POSTS)):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(POSTS, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    # 이미 추가된 경우 스킵
    if "상세 내용은" in html and "홈페이지에서 확인하기" in html:
        skipped += 1
        continue

    url, label = get_official(html)
    top_btn = make_top_btn(url, label)
    bottom_btn = make_bottom_btn(url, label)

    # ── 상단 버튼: <div class="post-body"> 바로 앞에 삽입 ──────────────────
    new_html = html.replace(
        '\n  <div class="post-body">',
        top_btn + '  <div class="post-body">',
        1
    )

    # ── 하단 버튼: "함께 보면 좋은 지원금" h2 바로 앞에 삽입 ─────────────
    new_html = new_html.replace(
        '\n    <h2>함께 보면 좋은 지원금</h2>',
        '\n' + bottom_btn + '    <h2>함께 보면 좋은 지원금</h2>',
        1
    )

    if new_html != html:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_html)
        updated += 1
    else:
        # fallback: 삽입 위치를 못 찾은 경우 로그
        print(f"  SKIP (pattern not found): {fname}")
        skipped += 1

print(f"\n완료: {updated}개 업데이트, {skipped}개 스킵")
