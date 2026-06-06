#!/usr/bin/env python3
import os, urllib.parse

BASE = "https://welfare.luckygrampus.com"
OUT = "/home/user/welfare/posts"

def enc(s):
    return urllib.parse.quote(s, safe='')

def make_post(filename, title, short_title, desc, og_desc, cat_label, bc_cat, bc_cat_url,
              official_url, official_label, body_html, faq_items, related_links, date="2026-06-06"):
    slug = filename.replace(".html", "")
    canon = f"{BASE}/posts/{enc(filename)}"
    crumb_json = f"""{{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"복지모아","item":"{BASE}/"}},
      {{"@type":"ListItem","position":2,"name":"{bc_cat}","item":"{BASE}/{bc_cat_url}"}},
      {{"@type":"ListItem","position":3,"name":"{title}","item":"{canon}"}}
    ]
  }}"""

    faq_schema_items = ",\n".join([f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}' for q,a in faq_items])
    faq_json = f"""{{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{faq_schema_items}]
  }}"""

    related_html = "\n".join([f'      <a href="{href}" class="related-card"><div class="rc-icon">{icon}</div><div class="rc-title">{label}</div></a>' for href, icon, label in related_links])

    faq_html = "\n".join([f"""    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">Q. {q} <span>▼</span></button>
      <div class="faq-a">A. {a}</div>
    </div>""" for q, a in faq_items])

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <link rel="sitemap" type="application/xml" href="../sitemap.xml">
  <meta charset="UTF-8">
  <meta name="naver-site-verification" content="7541a877bee52c44beb6410f16a62f585a44ad99" />
  <link rel="manifest" href="../manifest.json">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#1a6fc4">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 복지모아</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <link rel="alternate" hreflang="ko" href="{canon}">
  <link rel="alternate" hreflang="x-default" href="{canon}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{BASE}/og-default.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .post-wrap {{ max-width: 780px; margin: 0 auto; padding: 40px 20px; }}
    .post-header {{ margin-bottom: 28px; }}
    .post-label {{ font-size: 0.8rem; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }}
    .post-h1 {{ font-size: clamp(1.4rem, 3vw, 2rem); font-weight: 800; line-height: 1.35; color: var(--text); margin-bottom: 14px; }}
    .post-summary {{ background: var(--primary-light); border-left: 4px solid var(--primary); padding: 14px 18px; border-radius: 0 8px 8px 0; font-size: 0.95rem; color: var(--text); margin-bottom: 8px; line-height: 1.7; }}
    .post-summary strong {{ color: var(--primary); }}
    .post-body h2 {{ font-size: 1.2rem; font-weight: 800; margin: 32px 0 12px; padding-bottom: 8px; border-bottom: 2px solid var(--border); color: var(--text); }}
    .post-body h3 {{ font-size: 1rem; font-weight: 700; margin: 20px 0 8px; color: var(--text); }}
    .post-body p {{ font-size: 0.95rem; line-height: 1.8; color: #333; margin-bottom: 12px; }}
    .post-body ul, .post-body ol {{ padding-left: 22px; margin-bottom: 14px; }}
    .post-body li {{ font-size: 0.93rem; line-height: 1.8; color: #333; margin-bottom: 4px; }}
    .info-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9rem; }}
    .info-table th {{ background: var(--primary); color: #fff; padding: 10px 14px; text-align: left; font-weight: 700; }}
    .info-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); }}
    .info-table tr:nth-child(even) td {{ background: var(--bg); }}
    .step-box {{ counter-reset: step; }}
    .step {{ display: flex; gap: 14px; margin-bottom: 16px; }}
    .step-num {{ min-width: 32px; height: 32px; background: var(--primary); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0; margin-top: 2px; }}
    .step-content {{ flex: 1; }}
    .step-content strong {{ display: block; font-size: 0.95rem; font-weight: 700; margin-bottom: 4px; }}
    .step-content span {{ font-size: 0.88rem; color: var(--text-sub); line-height: 1.6; }}
    .faq-item {{ border: 1px solid var(--border); border-radius: 10px; margin-bottom: 10px; overflow: hidden; }}
    .faq-q {{ padding: 14px 18px; font-weight: 700; font-size: 0.93rem; cursor: pointer; background: var(--bg); display: flex; justify-content: space-between; align-items: center; border: none; width: 100%; text-align: left; font-family: var(--font); color: var(--text); }}
    .faq-a {{ padding: 12px 18px; font-size: 0.9rem; line-height: 1.7; color: var(--text-sub); display: none; border-top: 1px solid var(--border); }}
    .faq-item.open .faq-a {{ display: block; }}
    .faq-item.open .faq-q {{ background: var(--primary-light); color: var(--primary); }}
    .related-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .related-card {{ border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; transition: border-color 0.15s; text-decoration: none; display: block; }}
    .related-card:hover {{ border-color: var(--primary); }}
    .related-card .rc-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}
    .related-card .rc-title {{ font-size: 0.88rem; font-weight: 700; color: var(--text); line-height: 1.4; }}
    .highlight-box {{ background: #fff8e1; border: 1px solid #f4c842; border-radius: 10px; padding: 14px 18px; margin: 16px 0; font-size: 0.9rem; line-height: 1.7; }}
    .highlight-box strong {{ color: #c87820; }}
    @media (max-width: 600px) {{ .related-grid {{ grid-template-columns: 1fr; }} }}
  </style>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8518556382646891" crossorigin="anonymous"></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{desc}",
    "url": "{canon}",
    "datePublished": "{date}",
    "dateModified": "{date}",
    "inLanguage": "ko-KR",
    "author": {{"@type": "Organization", "name": "복지모아", "url": "{BASE}"}},
    "publisher": {{"@type": "Organization", "name": "복지모아", "url": "{BASE}"}},
    "image": "{BASE}/og-default.png"
  }}
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-8L1DP9KW1N"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-8L1DP9KW1N');</script>
  <script src="../js/ga-events.js" defer></script>
  <script type="application/ld+json">
  {crumb_json}
  </script>
  <script type="application/ld+json">
  {faq_json}
  </script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="logo"><span class="logo-icon">🏛️</span><span>복지모아</span></a>
    <nav class="site-nav">
      <a href="/">홈</a>
      <a href="../search.html">지원금 검색</a>
      <a href="../{bc_cat_url}">카테고리</a>
      <a href="/#categories">전체보기</a>
    </nav>
  </div>
</header>
<div style="text-align:center;padding:8px 0;background:#fff;border-bottom:1px solid #dde3ed;">
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8518556382646891" data-ad-slot="4593096138" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<div class="post-wrap">
  <div class="post-header">
    <div class="post-label">{cat_label}</div>
    <h1 class="post-h1">{title}</h1>
    <div class="post-summary"><strong>핵심 요약:</strong> {og_desc} ※ 정확한 금액·일정은 공식 사이트에서 확인하세요.</div>
    <div class="post-meta-date" style="font-size:0.8rem;color:#888;margin:8px 0 20px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
      <span>📅 자료 기준: 2026년</span>
      <span style="color:#ddd;">|</span>
      <span>출처: <a href="{official_url}" target="_blank" rel="noopener" style="color:#1a6fc4;text-decoration:none;">{official_label}</a></span>
    </div>
  </div>

  <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-8518556382646891" data-ad-slot="5445109426"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>

  <div class="post-body">
{body_html}

    <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-8518556382646891" data-ad-slot="5445109426"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>

    <h2>자주 묻는 질문 (FAQ)</h2>
{faq_html}

    <ins class="adsbygoogle" style="display:block; text-align:center;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-8518556382646891" data-ad-slot="5445109426"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>

    <h2>함께 보면 좋은 지원금</h2>
    <div class="related-grid">
{related_html}
    </div>
  </div>

  <div style="margin-top:36px;padding-top:24px;border-top:1px solid var(--border);font-size:0.82rem;color:#aaa;">※ 본 정보는 참고용입니다. 정확한 지원 금액·자격·신청 기간은 <a href="{official_url}" target="_blank" rel="noopener" style="color:var(--primary);">{official_label}</a> 또는 주민센터에서 반드시 확인하시기 바랍니다. (자료 기준: 2026년)</div>
</div>

<div class="banner-strip">
  <h2>다른 지원금도 확인해보세요</h2>
  <p>나이·지역·가구유형·소득을 입력하면 받을 수 있는 지원금 목록을 바로 확인할 수 있습니다.</p>
  <a href="../search.html" class="btn-primary">맞춤 지원금 검색 →</a>
</div>

<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <div class="footer-logo">🏛️ 복지모아</div>
      <p>정부 지원금·복지혜택 정보를<br>쉽고 빠르게 찾아드립니다.</p>
    </div>
    <div>
      <div style="font-weight:700;color:#dde3ed;margin-bottom:10px;">카테고리</div>
      <div class="footer-links">
        <a href="../청년-지원금.html">청년 지원금</a>
        <a href="../노인-복지.html">노인 복지</a>
        <a href="../장애인-복지.html">장애인 복지</a>
        <a href="../지역별-복지.html">지역별 복지</a>
        <a href="../기초생활수급.html">기초생활수급</a>
        <a href="../가족-출산-지원.html">가족·출산</a>
        <a href="../취업-교육-지원.html">취업·교육</a>
      </div>
    </div>
    <div>
      <div style="font-weight:700;color:#dde3ed;margin-bottom:10px;">바로가기</div>
      <div class="footer-links">
        <a href="../index.html">복지모아 홈</a>
        <a href="https://www.bokjiro.go.kr" target="_blank" rel="noopener noreferrer">복지로</a>
        <a href="https://www.gov.kr" target="_blank" rel="noopener noreferrer">정부24</a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 복지모아 · 본 사이트는 정보 제공 목적이며, 공식 지원금 신청은 각 부처 공식 사이트에서 하시기 바랍니다.</p>
  </div>
</footer>

<script>
function toggleFaq(btn) {{
  var item = btn.closest('.faq-item');
  item.classList.toggle('open');
  btn.setAttribute('aria-expanded', item.classList.contains('open'));
}}
</script>
<button id="back-to-top" aria-label="맨 위로" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<script>
(function(){{
  var btn = document.getElementById('back-to-top');
  window.addEventListener('scroll', function(){{
    btn.classList.toggle('visible', window.scrollY > 300);
  }}, {{passive: true}});
}})();
</script>
</body>
</html>"""
    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {filename}")

# ── POST 1: 국가건강검진 ──────────────────────────────────────────────────────
make_post(
    filename="국가건강검진-무료-2026.html",
    title="국가건강검진 무료 2026 — 대상·항목·예약 방법 총정리",
    short_title="국가건강검진 무료",
    desc="2026년 국가건강검진 무료 대상자·검진 항목·예약 방법을 총정리했습니다. 2년마다 받을 수 있는 일반건강검진부터 6대 암검진까지 한눈에 확인하세요.",
    og_desc="건강보험 가입자라면 2년마다 무료로 받을 수 있는 일반건강검진과 6대 암검진(위·대장·간·유방·자궁경부·폐암) 대상·항목·예약 방법을 정리했습니다.",
    cat_label="건강검진 · 의료지원",
    bc_cat="기초생활·저소득",
    bc_cat_url="기초생활수급.html",
    official_url="https://www.nhis.or.kr",
    official_label="국민건강보험공단",
    body_html="""    <h2>국가건강검진이란?</h2>
    <p>국가건강검진은 국민건강보험공단이 주관하는 무료 건강검진 제도입니다. <strong>건강보험 직장가입자·지역가입자·피부양자</strong> 및 <strong>의료급여 수급자</strong>를 대상으로 2년마다(일부 매년) 실시합니다.</p>
    <div class="highlight-box"><strong>💡 2026년 검진 대상:</strong> 짝수 출생연도(2000, 1998, 1996…)인 건강보험 가입자 및 피부양자가 2026년 일반건강검진 대상입니다. 홀수 연도 출생자는 2027년 대상입니다. 의료급여 수급자는 매년 검진 가능합니다.</div>

    <h2>검진 종류와 항목</h2>
    <table class="info-table">
      <tr><th>검진 종류</th><th>대상</th><th>주요 항목</th></tr>
      <tr><td>일반건강검진</td><td>건강보험 가입자(직장·지역), 피부양자, 의료급여 수급자</td><td>신체계측, 혈압, 혈당, 콜레스테롤, 간기능, 신장기능, 흉부X선, 구강검진 등</td></tr>
      <tr><td>위암검진</td><td>만 40세 이상 (2년마다)</td><td>위내시경 또는 위장조영검사</td></tr>
      <tr><td>대장암검진</td><td>만 50세 이상 (매년)</td><td>분변잠혈검사 → 이상 시 대장내시경</td></tr>
      <tr><td>간암검진</td><td>만 40세 이상 고위험군 (6개월마다)</td><td>복부초음파 + 혈청알파태아단백검사</td></tr>
      <tr><td>유방암검진</td><td>만 40세 이상 여성 (2년마다)</td><td>유방촬영술</td></tr>
      <tr><td>자궁경부암검진</td><td>만 20세 이상 여성 (2년마다)</td><td>자궁경부세포검사</td></tr>
      <tr><td>폐암검진</td><td>만 54~74세 흡연력 있는 고위험군 (매년)</td><td>저선량 흉부CT</td></tr>
    </table>

    <h2>예약 및 검진 방법</h2>
    <div class="step-box">
      <div class="step"><div class="step-num">1</div><div class="step-content"><strong>대상 여부 확인</strong><span>국민건강보험공단 앱(The건강보험) 또는 홈페이지(nhis.or.kr) → '건강검진' 메뉴에서 본인 검진 대상 여부 및 유효기간 확인</span></div></div>
      <div class="step"><div class="step-num">2</div><div class="step-content"><strong>검진기관 선택 및 예약</strong><span>nhis.or.kr → 건강iN → 검진기관 찾기에서 가까운 병·의원 검색 후 전화 또는 온라인 예약</span></div></div>
      <div class="step"><div class="step-num">3</div><div class="step-content"><strong>검진 당일 방문</strong><span>신분증 지참. 혈액검사 항목이 있으면 8시간 공복 필요. 검진비용은 무료(일부 선택항목 추가 비용 발생 가능)</span></div></div>
      <div class="step"><div class="step-num">4</div><div class="step-content"><strong>결과 확인</strong><span>검진 후 15~30일 이내 우편 통보. 국민건강보험 앱에서 디지털 결과 확인 가능</span></div></div>
    </div>

    <h2>검진비용은 무료인가요?</h2>
    <p>일반건강검진과 6대 암검진의 기본 항목은 <strong>전액 무료</strong>입니다. 단, 검진 결과 이상 소견으로 추가 검사가 필요한 경우 건강보험 본인부담금이 발생할 수 있습니다. 폐암검진의 경우 저선량 CT 비용 중 <strong>10%는 본인 부담</strong>입니다(의료급여 수급자 무료).</p>""",
    faq_items=[
        ("검진 유효기간이 지나면 어떻게 되나요?", "해당 연도 12월 31일까지 검진을 받지 않으면 소멸됩니다. 다음 대상 연도에 다시 검진 자격이 주어집니다."),
        ("직장 건강검진과 국가건강검진이 겹치면?", "직장에서 사업주 주관으로 건강검진을 받은 경우, 국가건강검진을 대체한 것으로 처리될 수 있습니다. 검진 항목과 실시 여부를 공단에 확인하세요."),
        ("피부양자도 무료로 받을 수 있나요?", "네. 직장가입자의 피부양자도 동일하게 2년마다 일반건강검진을 무료로 받을 수 있습니다."),
        ("암검진 대상자가 아닌데 받고 싶으면?", "대상 연령에 해당하지 않거나 검진 주기가 아닌 경우 개인비용으로 검진을 받아야 합니다. 단, 가족력 등 고위험군은 의사 소견에 따라 급여 적용이 가능할 수 있습니다."),
    ],
    related_links=[
        ("의료급여-2026.html", "🏥", "의료급여 — 저소득층 의료비 지원"),
        ("본인부담상한제-환급-2026.html", "💰", "본인부담상한제 — 과도한 의료비 환급"),
        ("암환자-의료비-지원금-2026.html", "🎗️", "암환자 의료비 지원금"),
        ("기초생활수급.html", "🔍", "기초생활 지원금 전체보기"),
    ],
)

# ── POST 2: 희귀질환자 의료비 지원 ──────────────────────────────────────────
make_post(
    filename="희귀질환자-의료비-지원-2026.html",
    title="희귀질환자 의료비 지원 2026 — 산정특례·본인부담 경감 총정리",
    short_title="희귀질환자 의료비 지원",
    desc="2026년 희귀질환자 의료비 지원 제도를 총정리했습니다. 산정특례 등록으로 본인부담 10% 적용, 추가 의료비 지원 신청 방법까지 안내합니다.",
    og_desc="희귀질환 산정특례 등록 시 외래·입원 본인부담 10%로 경감됩니다. 기초생활수급자·차상위 희귀질환자는 본인부담 0~5%까지 추가 지원받을 수 있습니다.",
    cat_label="희귀질환 · 의료지원",
    bc_cat="기초생활·저소득",
    bc_cat_url="기초생활수급.html",
    official_url="https://www.nhis.or.kr",
    official_label="국민건강보험공단",
    body_html="""    <h2>희귀질환 산정특례 제도란?</h2>
    <p>희귀질환으로 진단받은 환자가 등록 신청하면 <strong>건강보험 본인부담률을 10%</strong>로 낮춰주는 제도입니다. 일반 건강보험 외래 본인부담(30~60%)에 비해 크게 경감됩니다.</p>
    <div class="highlight-box"><strong>💡 산정특례 적용 기간:</strong> 최초 등록 후 <strong>5년간</strong> 적용됩니다. 5년 후 재등록 심사를 통해 연장 가능합니다. 중증 희귀질환의 경우 10년 적용 또는 영구 등록이 가능한 경우도 있습니다.</div>

    <h2>희귀질환자 의료비 지원 사업</h2>
    <p>산정특례와 별도로, <strong>저소득 희귀질환자</strong>에게는 건강보험 본인부담금·비급여 항목을 추가 지원하는 '희귀질환자 의료비 지원사업'이 있습니다.</p>
    <table class="info-table">
      <tr><th>구분</th><th>지원 대상</th><th>지원 내용</th></tr>
      <tr><td>건강보험 가입자</td><td>기준 중위소득 120% 이하 희귀질환자</td><td>본인부담금·간병비·보조기기 등 연간 최대 2,000만원 한도</td></tr>
      <tr><td>의료급여 수급자</td><td>의료급여 1·2종 희귀질환자</td><td>본인부담금 전액 지원</td></tr>
      <tr><td>산정특례 미등재 질환</td><td>희귀·난치성으로 확인된 경우</td><td>별도 심의 후 지원 여부 결정</td></tr>
    </table>

    <h2>신청 방법</h2>
    <div class="step-box">
      <div class="step"><div class="step-num">1</div><div class="step-content"><strong>희귀질환 진단 확인</strong><span>전문의에게 희귀질환 진단서(상병코드 확인) 발급. 질병관리청 희귀질환 목록(rare.nih.go.kr)에서 해당 질환 여부 확인</span></div></div>
      <div class="step"><div class="step-num">2</div><div class="step-content"><strong>산정특례 등록 신청</strong><span>국민건강보험공단 지사 방문 또는 The건강보험 앱에서 등록 신청. 진단서·의사 소견서 등 서류 제출</span></div></div>
      <div class="step"><div class="step-num">3</div><div class="step-content"><strong>의료비 지원 신청 (별도)</strong><span>주소지 관할 보건소에서 '희귀질환자 의료비 지원' 신청. 소득 기준 충족 여부 심사 후 지원 여부 결정</span></div></div>
      <div class="step"><div class="step-num">4</div><div class="step-content"><strong>지원금 수령</strong><span>진료비 영수증 등 제출 후 심사 완료 시 계좌 입금. 연 1회 또는 분기별 신청 가능</span></div></div>
    </div>

    <h2>지원 대상 질환</h2>
    <p>보건복지부 고시 기준으로 <strong>1,400여 개</strong> 희귀질환이 산정특례 등록 대상에 포함됩니다. 근육병, 루게릭병(ALS), 헌팅턴병, 고셔병, 파브리병 등이 대표적입니다. 정확한 질환 목록은 질병관리청 희귀질환 헬프라인(1588-7770)에서 확인하세요.</p>""",
    faq_items=[
        ("산정특례에 등록하면 모든 진료비가 10%인가요?", "등록된 희귀질환의 직접 관련 진료에 한해 10%가 적용됩니다. 희귀질환과 무관한 다른 질병 치료 시에는 일반 본인부담률이 적용됩니다."),
        ("비급여 항목도 지원받을 수 있나요?", "산정특례는 급여 항목에만 적용됩니다. 다만 희귀질환자 의료비 지원사업에서 저소득 환자에 한해 일부 비급여 항목도 지원합니다."),
        ("등록 후 5년이 지났는데 자동 연장되나요?", "자동 연장되지 않습니다. 만료 전 재등록 신청을 해야 하며, 의사 소견서 등 서류를 다시 제출해야 합니다."),
        ("미성년 자녀가 희귀질환인 경우 부모가 신청 가능한가요?", "네. 미성년자는 법정대리인(부모)이 대신 신청할 수 있습니다. 관련 서류에 법정대리인 서명이 필요합니다."),
    ],
    related_links=[
        ("의료급여-2026.html", "🏥", "의료급여 — 저소득층 의료비 지원"),
        ("본인부담상한제-환급-2026.html", "💰", "본인부담상한제 — 과도한 의료비 환급"),
        ("재난적-의료비-지원-2026.html", "🚨", "재난적 의료비 지원"),
        ("기초생활수급자-신청-2026.html", "📋", "기초생활수급자 신청 방법"),
    ],
)

# ── POST 3: 자활사업 ──────────────────────────────────────────────────────────
make_post(
    filename="자활사업-신청방법-2026.html",
    title="자활사업 신청 방법 2026 — 자활급여·자활근로 총정리",
    short_title="자활사업 신청",
    desc="2026년 자활사업 신청 방법을 총정리했습니다. 기초수급자·차상위계층이 자립할 수 있도록 자활근로, 취업 연계, 창업 지원을 제공하는 자활사업을 안내합니다.",
    og_desc="기초수급자·차상위계층 근로 능력자를 위한 자활사업입니다. 자활근로 참여 시 월 50~70만원 자활급여를 받으면서 기술·경력을 쌓아 자립을 준비할 수 있습니다.",
    cat_label="기초생활수급 · 자립지원",
    bc_cat="기초생활·저소득",
    bc_cat_url="기초생활수급.html",
    official_url="https://www.bokjiro.go.kr",
    official_label="복지로",
    body_html="""    <h2>자활사업이란?</h2>
    <p>자활사업은 근로 능력이 있는 저소득층이 스스로 자립할 수 있도록 <strong>일자리 제공·기술훈련·창업지원</strong>을 통해 탈빈곤을 돕는 제도입니다. 주민센터·지역자활센터를 통해 참여할 수 있습니다.</p>

    <h2>참여 대상</h2>
    <table class="info-table">
      <tr><th>구분</th><th>대상</th></tr>
      <tr><td>의무 참여</td><td>기초생활수급자 중 조건부수급자(근로 능력 있는 18~64세 수급자)</td></tr>
      <tr><td>희망 참여</td><td>차상위계층, 기초수급자 중 조건부과 제외자, 일반 저소득층</td></tr>
    </table>

    <h2>자활사업 유형</h2>
    <div class="step-box">
      <div class="step"><div class="step-num">1</div><div class="step-content"><strong>자활근로</strong><span>지역자활센터에서 운영하는 자활공동체·기업 참여. 간병, 집수리, 청소, 도시락, 세탁 등 다양한 업종. 월 약 50~70만원 내외 자활급여 지급</span></div></div>
      <div class="step"><div class="step-num">2</div><div class="step-content"><strong>취업 연계 프로그램</strong><span>취업성공패키지, 직업훈련 연계, 일자리 매칭 서비스. 취업 시 취업성공수당 최대 150만원 지급</span></div></div>
      <div class="step"><div class="step-num">3</div><div class="step-content"><strong>자활기업 창업 지원</strong><span>2인 이상이 모여 자활기업 설립 가능. 창업 초기 사업비·임차보증금·운영비 일부 지원</span></div></div>
      <div class="step"><div class="step-num">4</div><div class="step-content"><strong>자산형성지원</strong><span>희망키움통장·내일키움통장 연계. 저축액에 매칭 지원금 적립, 3년 후 목돈 수령 가능</span></div></div>
    </div>

    <h2>신청 방법</h2>
    <p>주소지 읍·면·동 <strong>주민센터</strong> 또는 <strong>지역자활센터</strong>에 방문하여 신청합니다. 복지로(bokjiro.go.kr)에서도 온라인 신청이 가능합니다. 신청 후 담당자 상담을 통해 참여 프로그램을 결정합니다.</p>
    <div class="highlight-box"><strong>💡 자활급여 지급 기준:</strong> 자활근로 참여 유형(시장진입형·사회서비스형·근로유지형)에 따라 급여 수준이 다릅니다. 정확한 급여액은 지역자활센터 담당자에게 확인하세요.</div>""",
    faq_items=[
        ("자활사업에 참여하면 기초수급 생계급여가 줄어드나요?", "자활근로 소득은 생계급여 산정 시 일부 소득공제가 적용됩니다. 전액 차감되지 않으므로 참여를 통해 실질 소득을 높일 수 있습니다."),
        ("자활사업 거부하면 어떻게 되나요?", "조건부수급자가 정당한 사유 없이 자활사업 참여를 거부하면 생계급여가 조건 불이행으로 중단될 수 있습니다."),
        ("차상위계층도 신청할 수 있나요?", "네. 차상위계층은 의무 참여 대상은 아니지만 희망 참여가 가능합니다. 자활급여 지급 여부와 금액은 담당자 상담 시 확인하세요."),
        ("자활기업을 만들면 어떤 혜택이 있나요?", "자활기업으로 인정되면 사업 초기 운영비, 국공유지 우선 임대, 공공기관 우선 구매 등의 혜택을 받을 수 있습니다."),
    ],
    related_links=[
        ("기초생활수급자-신청-2026.html", "📋", "기초생활수급자 신청 방법"),
        ("차상위계층-신청-방법-2026.html", "📄", "차상위계층 신청 방법"),
        ("국민취업지원제도-2026.html", "💼", "국민취업지원제도"),
        ("직업훈련-생계비-대출-2026.html", "🎓", "직업훈련 생계비 대출"),
    ],
)

# ── POST 4: 해산급여·장제급여 ─────────────────────────────────────────────────
make_post(
    filename="해산급여-장제급여-2026.html",
    title="해산급여·장제급여 2026 — 기초수급자 출산·사망 지원금",
    short_title="해산급여·장제급여",
    desc="2026년 기초생활수급자 해산급여(출산 지원금)와 장제급여(사망 지원금)를 총정리했습니다. 지급 금액, 신청 방법, 구비 서류를 확인하세요.",
    og_desc="기초수급자가 출산하면 해산급여 70만원(쌍둥이 140만원), 사망하면 장제급여 80만원을 지원합니다. 주민센터에서 출생·사망 신고 시 함께 신청 가능합니다.",
    cat_label="기초생활수급 · 급여안내",
    bc_cat="기초생활·저소득",
    bc_cat_url="기초생활수급.html",
    official_url="https://www.bokjiro.go.kr",
    official_label="복지로",
    body_html="""    <h2>해산급여란?</h2>
    <p>기초생활수급자(생계·의료·주거급여 수급자)가 출산했을 때 지급하는 출산 지원금입니다. <strong>1인당 70만원</strong>을 일시금으로 지급합니다.</p>
    <table class="info-table">
      <tr><th>구분</th><th>지급 금액</th></tr>
      <tr><td>단태아 출산</td><td>70만원</td></tr>
      <tr><td>쌍태아(쌍둥이) 출산</td><td>140만원 (1인당 70만원)</td></tr>
      <tr><td>삼태아 이상 출산</td><td>210만원 이상 (1인당 70만원)</td></tr>
    </table>
    <p>※ 위 금액은 2025년 기준입니다. 2026년 금액은 보건복지부 고시에 따라 변동될 수 있습니다.</p>

    <h2>장제급여란?</h2>
    <p>기초생활수급자가 사망했을 때 장례비용을 지원하는 급여입니다. <strong>80만원</strong>을 장제를 실제로 행하는 사람에게 지급합니다.</p>
    <div class="highlight-box"><strong>💡 장제급여 수령자:</strong> 사망한 수급자의 가족 또는 실제 장제를 치른 사람이 신청합니다. 장제를 행한 자가 수급자 가구가 아닌 경우에도 신청 가능합니다.</div>

    <h2>신청 방법</h2>
    <div class="step-box">
      <div class="step"><div class="step-num">1</div><div class="step-content"><strong>해산급여</strong><span>출생신고 시 읍·면·동 주민센터에서 동시 신청. 출생증명서, 통장 사본 지참. 신청 후 14일 이내 지급</span></div></div>
      <div class="step"><div class="step-num">2</div><div class="step-content"><strong>장제급여</strong><span>사망 신고 후 읍·면·동 주민센터에서 신청. 사망진단서, 장제를 행한 자 신분증, 통장 사본 지참</span></div></div>
    </div>

    <h2>자격 요건</h2>
    <ul>
      <li>해산급여: 생계급여·의료급여·주거급여 수급자가 출산한 경우 (교육급여만 받는 경우 제외)</li>
      <li>장제급여: 생계급여·의료급여·주거급여 수급자가 사망한 경우</li>
      <li>의료급여 수급자: 해산급여·장제급여 모두 적용</li>
    </ul>""",
    faq_items=[
        ("기초수급자가 아닌 차상위계층도 받을 수 있나요?", "해산급여와 장제급여는 기초생활수급자 중 생계·의료·주거급여 수급자에게만 지급됩니다. 차상위계층은 해당되지 않습니다."),
        ("해산급여는 첫만남이용권과 중복으로 받을 수 있나요?", "네. 해산급여는 기초생활보장 급여이고, 첫만남이용권은 별도 출산지원 제도이므로 중복 수령이 가능합니다. 부모급여도 함께 받을 수 있습니다."),
        ("출산 후 수급자격을 잃은 경우 소급 신청이 가능한가요?", "출산 당시 수급자였다면 이후 수급자격이 변경되더라도 해산급여를 신청할 수 있습니다. 출산일로부터 1년 이내에 신청하세요."),
        ("장제급여는 화장·매장 모두 적용되나요?", "네. 장례 방식(화장·매장·봉안 등)과 관계없이 장제급여 80만원이 지급됩니다."),
    ],
    related_links=[
        ("기초생활수급자-신청-2026.html", "📋", "기초생활수급자 신청 방법"),
        ("첫만남이용권-출산지원금-2026.html", "🎁", "첫만남이용권 출산지원금"),
        ("부모급여-신청-방법-2026.html", "👶", "부모급여 신청 방법"),
        ("한부모가족-지원금-2026.html", "👨‍👧", "한부모가족 지원금"),
    ],
)

# ── POST 5: 노인 안경 지원 ────────────────────────────────────────────────────
make_post(
    filename="노인-안경지원-2026.html",
    title="노인 안경 지원 2026 — 저소득 노인 안경 구입비 지원",
    short_title="노인 안경 지원",
    desc="2026년 저소득 노인 안경 구입비 지원 제도를 총정리했습니다. 기초수급자·차상위 노인은 건강보험 급여로 안경 구입비 일부를 지원받을 수 있습니다.",
    og_desc="기초수급자 등 저소득 노인은 건강보험 급여 보조기기 지원으로 안경·돋보기 구입비를 지원받을 수 있습니다. 만 65세 이상 지자체 별도 지원 사업도 있습니다.",
    cat_label="노인복지 · 보조기기",
    bc_cat="노인 복지",
    bc_cat_url="노인-복지.html",
    official_url="https://www.nhis.or.kr",
    official_label="국민건강보험공단",
    body_html="""    <h2>노인 안경 지원 제도 개요</h2>
    <p>노인의 시력 관련 지원은 크게 <strong>건강보험 보조기기 급여</strong>와 <strong>지자체 별도 지원사업</strong>으로 나뉩니다.</p>

    <h2>건강보험 보조기기 급여 (안경·돋보기)</h2>
    <table class="info-table">
      <tr><th>대상</th><th>지원 내용</th><th>급여 한도</th></tr>
      <tr><td>만 19세 이상 건강보험 가입자 (시력 교정 필요)</td><td>안경·콘택트렌즈 구입비 급여 적용</td><td>5년마다 1회, 최대 34,000원 지원 (본인부담 후 급여 청구)</td></tr>
      <tr><td>의료급여 수급자</td><td>안경 구입비 본인부담 없음 (1종) 또는 경감</td><td>동일 조건</td></tr>
    </table>
    <p>※ 위 급여 한도는 건강보험 기본 급여 기준이며, 실제 안경 가격은 이보다 높아 추가 비용이 발생할 수 있습니다.</p>

    <h2>지자체별 노인 안경 지원 사업</h2>
    <p>서울·경기·부산 등 일부 지자체에서 <strong>만 65세 이상 저소득 노인</strong>에게 안경 구입비를 추가 지원하는 사업을 운영합니다.</p>
    <table class="info-table">
      <tr><th>지자체</th><th>대상</th><th>지원 금액</th></tr>
      <tr><td>서울시</td><td>만 65세 이상 기초수급자·차상위</td><td>최대 10만원 (시·구별 상이)</td></tr>
      <tr><td>경기도</td><td>만 65세 이상 저소득 노인</td><td>최대 8~10만원 (시·군별 상이)</td></tr>
      <tr><td>기타 지자체</td><td>각 시·군·구 조례에 따라 상이</td><td>5~15만원 내외</td></tr>
    </table>
    <div class="highlight-box"><strong>💡 신청 방법:</strong> 거주 지역 읍·면·동 주민센터 또는 시·군·구청 복지과에 문의하세요. 안과 처방전과 안경원 영수증을 제출하면 환급 방식으로 지원받을 수 있습니다.</div>

    <h2>노인 틀니·임플란트 지원도 함께 확인하세요</h2>
    <p>만 65세 이상 건강보험 가입자는 틀니와 임플란트도 건강보험 급여 적용을 받을 수 있습니다. 본인부담률 30%로 상당한 비용을 절감할 수 있습니다.</p>""",
    faq_items=[
        ("안경 급여를 받으려면 어떻게 해야 하나요?", "안과 처방전을 받은 후 안경원에서 구입합니다. 안경원에서 건강보험 적용을 요청하면 급여 한도(34,000원)만큼 보험공단이 안경원에 직접 지급하고 차액을 본인이 부담합니다."),
        ("5년마다 1회라는 기준은 어떻게 계산하나요?", "이전 급여 청구일 기준 5년(60개월)이 지나면 다시 급여를 받을 수 있습니다. 건강보험 앱에서 본인의 최근 급여 이력을 확인하세요."),
        ("콘택트렌즈도 급여가 되나요?", "안과 전문의 처방이 있는 경우 콘택트렌즈도 급여 적용이 됩니다. 동일한 5년 1회, 34,000원 한도가 적용됩니다."),
        ("지자체 지원금과 건강보험 급여를 동시에 받을 수 있나요?", "일반적으로 중복 수령이 가능합니다. 단, 일부 지자체는 건강보험 급여 적용분을 제외한 잔액만 지원하는 경우도 있으니 주민센터에서 확인하세요."),
    ],
    related_links=[
        ("노인-틀니-임플란트-지원-2026.html", "🦷", "노인 틀니·임플란트 건강보험 지원"),
        ("노인-보청기-지원-2026.html", "👂", "노인 보청기 지원"),
        ("기초연금-신청-2026.html", "💰", "기초연금 신청 방법"),
        ("노인-복지.html", "🔍", "노인 복지 전체보기"),
    ],
)

print("Batch 1 done (5 posts)")
