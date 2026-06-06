#!/usr/bin/env python3
import os, re

WELFARE = "/home/user/welfare"

cat_additions = {
    "기초생활수급.html": [
        ("국가건강검진-무료-2026.html", "🔬", "국가건강검진 무료", "2년마다 무료 일반·암검진"),
        ("희귀질환자-의료비-지원-2026.html", "🧬", "희귀질환자 의료비 지원", "산정특례 본인부담 10%"),
        ("자활사업-신청방법-2026.html", "🌱", "자활사업 신청", "자활근로 월 50~70만원 급여"),
        ("해산급여-장제급여-2026.html", "📋", "해산·장제급여", "출산 70만원·사망 80만원"),
        ("결핵환자-지원금-2026.html", "💊", "결핵환자 지원금", "치료비 전액 무료 지원"),
        ("저소득층-법률지원-2026.html", "⚖️", "저소득층 법률 지원", "무료 법률 상담·소송 지원"),
    ],
    "노인-복지.html": [
        ("노인-안경지원-2026.html", "👓", "노인 안경 지원", "저소득 노인 안경 구입비"),
        ("노인-복지관서비스-2026.html", "🏛️", "노인 복지관 서비스", "무료 프로그램·식사·돌봄"),
        ("치매가족-지원서비스-2026.html", "🧠", "치매 가족 지원", "치매안심센터·단기보호 연계"),
        ("노인-재가서비스-2026.html", "🏠", "노인 재가서비스", "방문요양·목욕·주야간보호"),
    ],
    "가족-출산-지원.html": [
        ("입양아동-양육지원-2026.html", "💝", "입양아동 양육 지원", "입양 축하금 250만원 + 월 양육보조금"),
        ("기저귀-조제분유-지원-2026.html", "🍼", "기저귀·조제분유 지원", "월 기저귀 9만원+분유 10.6만원"),
        ("영유아-건강검진-2026.html", "👶", "영유아 건강검진", "8차 무료 건강검진"),
        ("아동급식지원-바우처-2026.html", "🍱", "아동급식 지원 바우처", "결식아동 1일 9,000원 지원"),
    ],
    "청년-지원금.html": [
        ("가족돌봄청년-지원금-2026.html", "🤲", "가족돌봄청년 지원", "영케어러 생활비·심리지원"),
        ("청소년-특별지원-2026.html", "🆘", "청소년 특별지원", "위기청소년 월 65만원 생활비"),
        ("학교밖청소년-지원금-2026.html", "📚", "학교밖청소년 지원", "검정고시·직업훈련·생활비"),
    ],
    "취업-교육-지원.html": [
        ("청년-취업성공패키지-2026.html", "🎯", "청년 취업성공패키지", "수당 최대 195만원+성공금 150만원"),
        ("농어업인-연금보험료-지원-2026.html", "🌾", "농어업인 연금보험료 지원", "국민연금 보험료 50% 감면"),
        ("방과후학교-자유수강권-2026.html", "🏫", "방과후학교 자유수강권", "저소득 학생 연 최대 60만원"),
        ("산재보험-급여-신청-2026.html", "🦺", "산재보험 급여 신청", "치료비 전액+임금 70% 휴업급여"),
        ("중장년-재취업-지원-2026.html", "👔", "중장년 재취업 지원", "50·60대 취업연계·고용장려금"),
    ],
    "장애인-복지.html": [
        ("장애인-직업재활서비스-2026.html", "💼", "장애인 직업재활 서비스", "직업훈련·취업 알선·수당"),
        ("장애인-주거편의지원-2026.html", "🏗️", "장애인 주거편의 지원", "편의시설 설치비 최대 380만원"),
        ("장애학생-교육지원-2026.html", "🎓", "장애학생 교육 지원", "특수교육 무료+치료지원 월 14만원"),
    ],
}

def make_card(post_file, icon, title, desc):
    return (
        f'    <a href="posts/{post_file}" class="post-card">\n'
        f'      <div class="pc-icon">{icon}</div>\n'
        f'      <div class="pc-title">{title}</div>\n'
        f'      <div class="pc-desc">{desc}</div>\n'
        f'    </a>'
    )

for cat_file, posts in cat_additions.items():
    cat_path = os.path.join(WELFARE, cat_file)
    with open(cat_path, "r", encoding="utf-8") as f:
        html = f.read()

    cards_html = "\n".join([make_card(pf, ic, ti, de) for pf, ic, ti, de in posts])

    # post-card 그리드 닫히는 </div> 직전에 삽입 (마지막 post-card 뒤)
    # "</div>\n\n  <!-- 다른 카테고리" 패턴 앞에 삽입
    pattern = r'(</div>\s*\n\s*<!--\s*다른 카테고리)'
    replacement = cards_html + "\n\\1"
    new_html, count = re.subn(pattern, replacement, html, count=1)

    if count == 0:
        # 두 번째 fallback: 마지막 post-card </a> 뒤 </div> 앞
        pattern2 = r'(    </a>\n</div>)'
        def last_match_replace(m):
            return m.group(0)  # dummy
        # 마지막 post-card 블록 찾아 그 뒤에 삽입
        idx = html.rfind('class="post-card"')
        if idx != -1:
            end = html.find('</a>', idx) + 4
            new_html = html[:end] + "\n" + cards_html + html[end:]
            count = 1
        else:
            new_html = html
            print(f"WARNING: no insertion point in {cat_file}")

    if count > 0 and new_html != html:
        with open(cat_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Updated: {cat_file} (+{len(posts)} cards)")
    else:
        print(f"NO CHANGE: {cat_file} (pattern not found)")
