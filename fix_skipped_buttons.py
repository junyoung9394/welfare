#!/usr/bin/env python3
import os, re

POSTS = "/home/user/welfare/posts"

LABEL_MAP = {
    "work.go.kr":    "고용24",
    "nhis.or.kr":    "국민건강보험공단",
    "nps.or.kr":     "국민연금공단",
    "myhome.go.kr":  "마이홈포털",
    "kosaf.go.kr":   "한국장학재단",
    "hometax.go.kr": "홈택스",
    "kpass.co.kr":   "케이패스",
    "bokjiro.go.kr": "복지로",
}

SKIPPED = [
    "강원도-복지-지원금-2026.html",
    "경북도-복지-지원금-2026.html",
    "광주시-복지-지원금-2026.html",
    "소상공인-복지-동시-활용-2026.html",
    "장애인연금-탈락-이유-2026.html",
    "차상위계층-탈락-이유-2026.html",
    "청년내일저축계좌-탈락-이유-2026.html",
    "충남도-복지-지원금-2026.html",
    "충북도-복지-지원금-2026.html",
    "한부모가족-지원금-탈락-이유-2026.html",
]

def get_official(html):
    # footer 패턴 1
    m = re.search(r'정확한 지원 금액·자격·신청 기간은 <a href="([^"]+)"[^>]*>([^<]+)</a>', html)
    if m:
        url = m.group(1).strip()
        for domain, label in LABEL_MAP.items():
            if domain in url:
                return url, label
        return url, m.group(2).strip()
    # footer 패턴 2 (구형)
    m = re.search(r'출처:.*?<a href="([^"]+)"', html)
    if m:
        url = m.group(1).strip()
        for domain, label in LABEL_MAP.items():
            if domain in url:
                return url, label
    return "https://www.bokjiro.go.kr", "복지로"

def make_top_btn(url, label):
    return (
        f'<div style="margin:20px 0 28px;text-align:center;">\n'
        f'  <a href="{url}" target="_blank" rel="noopener"\n'
        f'     style="display:inline-flex;align-items:center;gap:8px;'
        f'background:#1a6fc4;color:#fff;padding:13px 28px;border-radius:10px;'
        f'text-decoration:none;font-weight:700;font-size:0.97rem;'
        f'box-shadow:0 3px 10px rgba(26,111,196,0.28);">\n'
        f'    🔗 상세 내용은 {label} 홈페이지에서 확인하기 →\n'
        f'  </a>\n'
        f'  <p style="font-size:0.76rem;color:#aaa;margin:7px 0 0;">'
        f'공식 사이트에서 최신 지원 금액 및 신청 기간을 꼭 확인하세요</p>\n'
        f'</div>\n'
    )

def make_bottom_btn(url, label):
    return (
        f'<div style="background:#f0f7ff;border:1.5px solid #b8d8f8;'
        f'border-radius:12px;padding:18px 20px;margin:28px 0 16px;text-align:center;">\n'
        f'  <p style="margin:0 0 10px;font-size:0.9rem;color:#444;font-weight:600;">'
        f'📋 지원 자격·신청 기간은 공식 사이트에서 확인하세요</p>\n'
        f'  <a href="{url}" target="_blank" rel="noopener"\n'
        f'     style="display:inline-block;background:#1a6fc4;color:#fff;'
        f'padding:11px 26px;border-radius:8px;text-decoration:none;font-weight:700;font-size:0.93rem;">\n'
        f'    🏛️ {label} 공식 사이트 바로가기\n'
        f'  </a>\n'
        f'</div>\n'
    )

for fname in SKIPPED:
    fpath = os.path.join(POSTS, fname)
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fname}")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    if "상세 내용은" in html and "홈페이지에서 확인하기" in html:
        print(f"ALREADY DONE: {fname}")
        continue

    url, label = get_official(html)
    top = make_top_btn(url, label)
    bot = make_bottom_btn(url, label)

    new_html = html

    # 상단 버튼: 첫 번째 <h2> 태그 바로 앞에 삽입
    new_html = re.sub(r'(<h2[^>]*>)', top + r'\1', new_html, count=1)

    # 하단 버튼: "함께 보면" h2/h3 앞, 없으면 footer disclaimer 앞에 삽입
    if re.search(r'<h[23][^>]*>함께 보면', new_html):
        new_html = re.sub(r'(<h[23][^>]*>함께 보면)', bot + r'\1', new_html, count=1)
    else:
        # footer disclaimer 앞에 삽입
        new_html = new_html.replace(
            '※ 본 정보는 참고용입니다.',
            bot + '※ 본 정보는 참고용입니다.',
            1
        )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Updated: {fname}")

print("\n완료!")
