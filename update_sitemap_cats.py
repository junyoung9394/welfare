#!/usr/bin/env python3
import urllib.parse, re, os

BASE = "https://welfare.luckygrampus.com"
WELFARE = "/home/user/welfare"

# ── 1. Sitemap 업데이트 ────────────────────────────────────────────────────────
new_posts = [
    "국가건강검진-무료-2026.html",
    "희귀질환자-의료비-지원-2026.html",
    "자활사업-신청방법-2026.html",
    "해산급여-장제급여-2026.html",
    "노인-안경지원-2026.html",
    "노인-복지관서비스-2026.html",
    "치매가족-지원서비스-2026.html",
    "입양아동-양육지원-2026.html",
    "가족돌봄청년-지원금-2026.html",
    "청년-취업성공패키지-2026.html",
    "장애인-직업재활서비스-2026.html",
    "장애인-주거편의지원-2026.html",
    "결핵환자-지원금-2026.html",
    "농어업인-연금보험료-지원-2026.html",
    "아동급식지원-바우처-2026.html",
    "방과후학교-자유수강권-2026.html",
    "학교밖청소년-지원금-2026.html",
    "산재보험-급여-신청-2026.html",
    "기저귀-조제분유-지원-2026.html",
    "영유아-건강검진-2026.html",
    "청소년-특별지원-2026.html",
    "장애학생-교육지원-2026.html",
    "저소득층-법률지원-2026.html",
    "중장년-재취업-지원-2026.html",
    "노인-재가서비스-2026.html",
]

sitemap_entries = "\n".join([
    f"""  <url>
    <loc>{BASE}/posts/{urllib.parse.quote(f, safe='')}</loc>
    <lastmod>2026-06-06</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>"""
    for f in new_posts
])

sitemap_path = os.path.join(WELFARE, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("</urlset>", sitemap_entries + "\n\n</urlset>")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Sitemap updated (+{len(new_posts)} entries)")

# ── 2. 카테고리 페이지에 포스트 카드 추가 ────────────────────────────────────
# 각 카테고리 파일에 삽입할 포스트 카드 목록
# 형식: (카테고리파일, 포스트파일, 이모지, 제목)
cat_additions = {
    "기초생활수급.html": [
        ("국가건강검진-무료-2026.html", "🔬", "국가건강검진 무료 2026 — 대상·항목·예약 방법 총정리"),
        ("희귀질환자-의료비-지원-2026.html", "🧬", "희귀질환자 의료비 지원 2026 — 산정특례·본인부담 경감"),
        ("자활사업-신청방법-2026.html", "🌱", "자활사업 신청 방법 2026 — 자활급여·자활근로 총정리"),
        ("해산급여-장제급여-2026.html", "📋", "해산급여·장제급여 2026 — 기초수급자 출산·사망 지원"),
        ("결핵환자-지원금-2026.html", "💊", "결핵환자 지원금 2026 — 치료비·생활비 무료 지원"),
        ("저소득층-법률지원-2026.html", "⚖️", "저소득층 법률 지원 2026 — 무료 법률 상담·소송 지원"),
    ],
    "노인-복지.html": [
        ("노인-안경지원-2026.html", "👓", "노인 안경 지원 2026 — 저소득 노인 안경 구입비 지원"),
        ("노인-복지관서비스-2026.html", "🏛️", "노인 복지관 서비스 2026 — 무료 프로그램·식사·돌봄"),
        ("치매가족-지원서비스-2026.html", "🧠", "치매 가족 지원 서비스 2026 — 돌봄 부담 줄이는 방법"),
        ("노인-재가서비스-2026.html", "🏠", "노인 재가서비스 2026 — 방문요양·방문목욕·주야간보호"),
    ],
    "가족-출산-지원.html": [
        ("입양아동-양육지원-2026.html", "💝", "입양아동 양육 지원 2026 — 입양 지원금·의료비·교육비"),
        ("기저귀-조제분유-지원-2026.html", "🍼", "기저귀·조제분유 지원 2026 — 저소득 영아 가정 지원"),
        ("영유아-건강검진-2026.html", "👶", "영유아 건강검진 2026 — 무료 검진 시기·항목 총정리"),
        ("아동급식지원-바우처-2026.html", "🍱", "아동급식 지원 바우처 2026 — 결식 아동 급식 지원"),
    ],
    "청년-지원금.html": [
        ("가족돌봄청년-지원금-2026.html", "🤲", "가족돌봄청년(영케어러) 지원금 2026 — 지원 내용 총정리"),
        ("청소년-특별지원-2026.html", "🆘", "청소년 특별지원 2026 — 위기 청소년 생활·의료·학업 지원"),
        ("학교밖청소년-지원금-2026.html", "📚", "학교 밖 청소년 지원금 2026 — 검정고시·취업·생활비"),
    ],
    "취업-교육-지원.html": [
        ("청년-취업성공패키지-2026.html", "🎯", "청년 취업성공패키지 2026 — 신청 자격·수당·참여 방법"),
        ("농어업인-연금보험료-지원-2026.html", "🌾", "농어업인 연금보험료 지원 2026 — 국민연금 50% 감면"),
        ("방과후학교-자유수강권-2026.html", "🏫", "방과후학교 자유수강권 2026 — 저소득층 학생 교육비 지원"),
        ("산재보험-급여-신청-2026.html", "🦺", "산재보험 급여 신청 2026 — 요양·휴업·장해급여 총정리"),
        ("중장년-재취업-지원-2026.html", "👔", "중장년 재취업 지원 2026 — 50·60대 취업 지원금 총정리"),
    ],
    "장애인-복지.html": [
        ("장애인-직업재활서비스-2026.html", "💼", "장애인 직업재활 서비스 2026 — 취업 지원·훈련·수당"),
        ("장애인-주거편의지원-2026.html", "🏗️", "장애인 주거편의 지원 2026 — 편의시설 설치비 지원"),
        ("장애학생-교육지원-2026.html", "🎓", "장애학생 교육 지원 2026 — 특수교육·치료지원·방과후"),
    ],
}

def make_card(post_file, emoji, title):
    return f'''    <a class="benefit-card" href="posts/{post_file}">
      <span class="benefit-icon">{emoji}</span>
      <div class="benefit-info">
        <div class="benefit-title">{title}</div>
      </div>
    </a>'''

for cat_file, posts in cat_additions.items():
    cat_path = os.path.join(WELFARE, cat_file)
    with open(cat_path, "r", encoding="utf-8") as f:
        html = f.read()

    # </main> 앞에 카드를 추가할 위치 탐색 — benefit-grid 마지막 카드 다음에 삽입
    cards_html = "\n".join([make_card(pf, em, ti) for pf, em, ti in posts])

    # benefit-grid 닫히는 </div> 바로 앞에 삽입
    pattern = r'(  </div>\s*</section>\s*</main>)'
    replacement = cards_html + "\n" + r'\1'
    new_html, count = re.subn(pattern, replacement, html, count=1)
    if count == 0:
        # fallback: </main> 앞에 삽입
        new_html = html.replace("</main>", cards_html + "\n</main>", 1)

    with open(cat_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Updated: {cat_file} (+{len(posts)} cards)")

print("\nAll done!")
