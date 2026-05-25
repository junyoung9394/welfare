"""
Claude API를 사용해 새 복지 포스트 HTML을 자동 생성합니다.

사용법:
  python scripts/generate_post.py "청년 전세대출 2026"
  python scripts/generate_post.py "청년 전세대출 2026" --cat 청년
  python scripts/generate_post.py "청년 전세대출 2026" --related "청년-월세-지원금-2026.html" "청년-주거급여-2026.html"

필요 환경변수:
  ANTHROPIC_API_KEY   Claude API 키

선택 환경변수:
  POST_AUTHOR         기본값 '복지모아 편집팀'
"""

import argparse
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("anthropic 패키지가 없습니다. 설치: pip install anthropic")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "posts"
BASE_URL = "https://welfare.luckygrampus.com"
KST = timezone(timedelta(hours=9))

ADSENSE_PUB = "ca-pub-8518556382646891"
ADSENSE_SLOTS = {
    "top": "4593096138",
    "mid": "5445109426",
}
GA_ID = "G-8L1DP9KW1N"
NAVER_VERIFY = "7541a877bee52c44beb6410f16a62f585a44ad99"

CATEGORY_MAP = {
    "청년": ("청년-지원금.html", "청년 지원금"),
    "노인": ("노인-복지.html", "노인 복지"),
    "장애인": ("장애인-복지.html", "장애인 복지"),
    "지역": ("지역별-복지.html", "지역별 복지"),
    "지역별": ("지역별-복지.html", "지역별 복지"),
    "기초생활": ("search.html?cat=기초생활", "기초생활수급"),
    "소상공인": ("search.html?cat=소상공인", "소상공인 지원"),
    "바우처": ("search.html?cat=바우처", "복지바우처"),
}


def detect_category(keyword: str) -> str:
    for cat in CATEGORY_MAP:
        if cat in keyword:
            return cat
    return "청년"  # 기본값


def slugify(text: str) -> str:
    """키워드를 파일명 슬러그로 변환"""
    text = text.strip()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w가-힣-]', '', text)
    return text


def build_system_prompt() -> str:
    return """당신은 한국 정부 복지·지원금 정보를 전문으로 다루는 웹사이트 '복지모아'의 SEO 최적화 콘텐츠 작성자입니다.

규칙:
1. 반드시 HTML만 출력하세요. 마크다운, 설명 텍스트, 코드 블록(```html ... ```) 없이 순수 HTML만.
2. 아래 제공되는 HTML 템플릿 구조를 정확히 따르세요. 플레이스홀더를 실제 콘텐츠로 채우세요.
3. 내용은 2026년 기준 최신 정보로 작성하되, 공식 출처에서 확인하라는 면책 문구를 항상 포함하세요.
4. 제목은 SEO를 고려해 키워드를 앞에 배치하고 '2026'을 포함하세요.
5. FAQ는 실제 사용자가 검색할 법한 질문 4~5개로 구성하세요.
6. 포스트 본문은 1200자 이상으로 충실하게 작성하세요.
7. 정보의 구체성: 금액, 기간, 나이 등 수치를 최대한 구체적으로 작성하세요.
"""


def build_user_prompt(keyword: str, cat: str, related: list[str], today: str) -> str:
    cat_file, cat_name = CATEGORY_MAP.get(cat, ("청년-지원금.html", "청년 지원금"))
    slug = slugify(keyword)
    filename = f"{slug}-2026.html" if "2026" not in slug else f"{slug}.html"
    encoded_filename = urllib.parse.quote(filename, safe='.-')
    canonical_url = f"{BASE_URL}/posts/{encoded_filename}"

    # 관련 포스트 HTML 생성
    related_cards_html = ""
    for rfile in related[:4]:
        rname = Path(rfile).stem.replace('-', ' ')
        related_cards_html += f'      <a href="{rfile}" class="related-card"><div class="rc-icon">📋</div><div class="rc-title">{rname}</div></a>\n'
    if not related_cards_html:
        related_cards_html = """      <a href="../search.html" class="related-card"><div class="rc-icon">🔍</div><div class="rc-title">맞춤 지원금 전체 검색</div></a>
      <a href="../{cat_file}" class="related-card"><div class="rc-icon">📋</div><div class="rc-title">{cat_name} 전체 보기</div></a>
""".format(cat_file=cat_file, cat_name=cat_name)

    template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="naver-site-verification" content="{NAVER_VERIFY}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}} | 복지모아</title>
  <meta name="description" content="{{META_DESCRIPTION}}">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{{TITLE}} | 복지모아">
  <meta property="og:description" content="{{META_DESCRIPTION}}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{BASE_URL}/og-default.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
  <link rel="manifest" href="../manifest.json">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#1a6fc4">
  <link rel="stylesheet" href="../css/style.css">
  <style>
    .post-wrap {{ max-width: 780px; margin: 0 auto; padding: 40px 20px; }}
    .post-header {{ margin-bottom: 28px; }}
    .post-label {{ font-size: 0.8rem; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }}
    .post-h1 {{ font-size: clamp(1.4rem, 3vw, 2rem); font-weight: 800; line-height: 1.35; color: var(--text); margin-bottom: 14px; }}
    .post-summary {{ background: var(--primary-light); border-left: 4px solid var(--primary); padding: 14px 18px; border-radius: 0 8px 8px 0; font-size: 0.95rem; color: var(--text); margin-bottom: 24px; line-height: 1.7; }}
    .post-summary strong {{ color: var(--primary); }}
    .post-body h2 {{ font-size: 1.2rem; font-weight: 800; margin: 32px 0 12px; padding-bottom: 8px; border-bottom: 2px solid var(--border); color: var(--text); }}
    .post-body p {{ font-size: 0.95rem; line-height: 1.8; color: #333; margin-bottom: 12px; }}
    .post-body ul, .post-body ol {{ padding-left: 22px; margin-bottom: 14px; }}
    .post-body li {{ font-size: 0.93rem; line-height: 1.8; color: #333; margin-bottom: 4px; }}
    .info-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9rem; }}
    .info-table th {{ background: var(--primary); color: #fff; padding: 10px 14px; text-align: left; font-weight: 700; }}
    .info-table td {{ padding: 10px 14px; border-bottom: 1px solid var(--border); }}
    .info-table tr:nth-child(even) td {{ background: var(--bg); }}
    .step {{ display: flex; gap: 14px; margin-bottom: 16px; }}
    .step-num {{ min-width: 32px; height: 32px; background: var(--primary); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; flex-shrink: 0; margin-top: 2px; }}
    .step-content {{ flex: 1; }}
    .step-content strong {{ display: block; font-size: 0.95rem; font-weight: 700; margin-bottom: 4px; }}
    .step-content span {{ font-size: 0.88rem; color: var(--text-sub); line-height: 1.6; }}
    .faq-item {{ border: 1px solid var(--border); border-radius: 10px; margin-bottom: 10px; overflow: hidden; }}
    .faq-q {{ padding: 14px 18px; font-weight: 700; font-size: 0.93rem; cursor: pointer; background: var(--bg); display: flex; justify-content: space-between; align-items: center; }}
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
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB}" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
<script src="../js/ga-events.js" defer></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{{TITLE}}",
    "description": "{{META_DESCRIPTION}}",
    "datePublished": "{today}",
    "dateModified": "{today}",
    "author": {{"@type": "Organization", "name": "복지모아"}},
    "publisher": {{"@type": "Organization", "name": "복지모아", "url": "{BASE_URL}"}},
    "mainEntityOfPage": "{canonical_url}"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"복지모아","item":"{BASE_URL}/"}},
      {{"@type":"ListItem","position":2,"name":"{cat_name}","item":"{BASE_URL}/{cat_file}"}},
      {{"@type":"ListItem","position":3,"name":"{{TITLE}}","item":"{canonical_url}"}}
    ]
  }}
  </script>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="logo"><span class="logo-icon">🏛️</span><span>복지모아</span></a>
    <nav class="site-nav">
      <a href="/">홈</a>
      <a href="../search.html">지원금 검색</a>
      <a href="../{cat_file}" class="active">{cat_name}</a>
      <a href="/#categories">카테고리</a>
    </nav>
  </div>
</header>
<div style="text-align:center;padding:8px 0;background:#fff;border-bottom:1px solid #dde3ed;">
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="{ADSENSE_PUB}"
     data-ad-slot="{ADSENSE_SLOTS['top']}"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>
<div class="post-wrap">
  <div class="post-header">
    <div class="post-label">{{POST_LABEL}}</div>
    <h1 class="post-h1">{{TITLE}}</h1>
    <div class="post-summary"><strong>핵심 요약:</strong> {{SUMMARY}}</div>
  </div>
  <ins class="adsbygoogle"
       style="display:block; text-align:center;"
       data-ad-layout="in-article"
       data-ad-format="fluid"
       data-ad-client="{ADSENSE_PUB}"
       data-ad-slot="{ADSENSE_SLOTS['mid']}"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  <div class="post-body">
    {{BODY_CONTENT}}

    <!-- AdSense 인아티클 하단 -->
    <ins class="adsbygoogle"
    style="display:block; text-align:center;"
    data-ad-layout="in-article"
    data-ad-format="fluid"
    data-ad-client="{ADSENSE_PUB}"
    data-ad-slot="{ADSENSE_SLOTS['mid']}"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>

    <h2>함께 보면 좋은 지원금</h2>
    <div class="related-grid">
{related_cards_html}    </div>
  </div>
  <div style="margin-top:36px;padding-top:24px;border-top:1px solid var(--border);font-size:0.82rem;color:#aaa;">
    ※ 본 정보는 참고용입니다. 정확한 지원 금액·자격·신청 기간은 <a href="https://www.bokjiro.go.kr" target="_blank" rel="noopener" style="color:var(--primary);">복지로 공식 사이트</a> 또는 주민센터에서 반드시 확인하시기 바랍니다.
  </div>
</div>
<div class="banner-strip">
  <h2>다른 지원금도 확인해보세요</h2>
  <p>나이·지역·가구유형·소득을 입력하면 받을 수 있는 지원금 목록을 바로 확인할 수 있습니다.</p>
  <a href="../search.html" class="btn-primary">맞춤 지원금 검색 →</a>
</div>
<footer class="site-footer">
  <div class="footer-inner">
    <div><div class="footer-logo">🏛️ 복지모아</div><p>정부 지원금·복지혜택 정보를<br>쉽고 빠르게 찾아드립니다.</p></div>
    <div><div style="font-weight:700;color:#dde3ed;margin-bottom:10px;">카테고리</div><div class="footer-links"><a href="../청년-지원금.html">청년 지원금</a><a href="../노인-복지.html">노인 복지</a><a href="../장애인-복지.html">장애인 복지</a><a href="../지역별-복지.html">지역별 복지</a><a href="../search.html?cat=기초생활">기초생활수급</a><a href="../search.html?cat=소상공인">소상공인 지원</a></div></div>
    <div><div style="font-weight:700;color:#dde3ed;margin-bottom:10px;">바로가기</div><div class="footer-links"><a href="../index.html">복지모아 홈</a><a href="https://www.bokjiro.go.kr" target="_blank" rel="noopener">복지로</a><a href="https://www.gov.kr" target="_blank" rel="noopener">정부24</a></div></div>
  </div>
  <div class="footer-bottom"><p>© 2026 복지모아 · 본 사이트는 정보 제공 목적이며, 공식 지원금 신청은 각 부처 공식 사이트에서 하시기 바랍니다.</p></div>
</footer>
<script>
function toggleFaq(btn) {{
  var item = btn.closest('.faq-item');
  item.classList.toggle('open');
}}
document.querySelectorAll('.faq-q').forEach(function(el) {{
  el.addEventListener('click', function() {{ toggleFaq(this); }});
}});
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

    return f"""다음 키워드로 복지모아 웹사이트 포스트 HTML을 작성해주세요:

키워드: {keyword}
카테고리: {cat_name}
오늘 날짜: {today}

아래 HTML 템플릿의 {{PLACEHOLDER}} 부분을 실제 콘텐츠로 채워서 완성된 HTML을 출력하세요.

채워야 할 플레이스홀더:
- {{TITLE}}: SEO 최적화 제목 (키워드 포함, 60자 이내, | 복지모아 제외)
- {{META_DESCRIPTION}}: 메타 설명 (150자 이내, 핵심 정보 포함)
- {{POST_LABEL}}: 카테고리명 · 담당부처 (예: "청년 지원 · 국토교통부")
- {{SUMMARY}}: 핵심 요약 1~2문장 (※ 정확한 정보는 공식 사이트 확인 안내 포함)
- {{BODY_CONTENT}}: 본문 HTML (아래 구조 필수 포함)

{{BODY_CONTENT}} 필수 구조:
1. <h2>신청 자격, 나는 해당될까?</h2> + <table class="info-table"> (대상/조건/금액 등)
2. <h2>지원 금액 및 혜택</h2> + 구체적 수치가 있는 표 또는 항목
3. <h2>신청 방법 (단계별)</h2> + <div class="step"> × 4~5개
4. <h2>자주 묻는 질문 (FAQ)</h2> + <div class="faq-item"> × 4개
   (각 faq-item 구조: <div class="faq-q">질문 <span>＋</span></div><div class="faq-a">답변</div>)
5. 중간에 <ins class="adsbygoogle" ...> 인아티클 광고 1개 삽입 (mid 슬롯)

템플릿:
{template}"""


def generate_post(keyword: str, cat: str, related: list[str]) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("오류: ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    today = datetime.now(KST).strftime('%Y-%m-%d')

    print(f"Claude API 호출 중... (키워드: {keyword})")
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8192,
        system=build_system_prompt(),
        messages=[
            {"role": "user", "content": build_user_prompt(keyword, cat, related, today)}
        ]
    )

    html = message.content[0].text.strip()

    # 코드 블록 래퍼 제거 (모델이 가끔 붙임)
    if html.startswith("```"):
        html = re.sub(r'^```[^\n]*\n', '', html)
        html = re.sub(r'\n```$', '', html)

    return html


def save_post(html: str, keyword: str) -> Path:
    slug = slugify(keyword)
    filename = f"{slug}-2026.html" if "2026" not in slug else f"{slug}.html"
    out_path = POSTS_DIR / filename

    if out_path.exists():
        backup = out_path.with_suffix(f".bak.html")
        out_path.rename(backup)
        print(f"기존 파일 백업: {backup.name}")

    out_path.write_text(html, encoding='utf-8')
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Claude API로 복지 포스트 자동 생성")
    parser.add_argument("keyword", help="포스트 주제 키워드 (예: '청년 전세대출 2026')")
    parser.add_argument("--cat", default=None,
                        help="카테고리 (청년/노인/장애인/지역별/기초생활/소상공인/바우처). 미입력시 자동 감지.")
    parser.add_argument("--related", nargs="*", default=[],
                        help="관련 포스트 파일명 (최대 4개, 예: 청년-월세-지원금-2026.html)")
    parser.add_argument("--dry-run", action="store_true",
                        help="파일 저장 없이 HTML을 stdout으로 출력")
    args = parser.parse_args()

    cat = args.cat or detect_category(args.keyword)
    html = generate_post(args.keyword, cat, args.related)

    if args.dry_run:
        print(html)
        return

    out_path = save_post(html, args.keyword)
    print(f"\n포스트 생성 완료: {out_path}")
    print(f"URL: {BASE_URL}/posts/{urllib.parse.quote(out_path.name, safe='.-')}")
    print("\n다음 단계:")
    print("  1. 생성된 파일을 검토 후 수정")
    print("  2. git add posts/<파일명> && git commit -m 'feat: 새 포스트 추가'")
    print("  3. git push → GitHub Actions가 sitemap.xml / feed.xml 자동 갱신")


if __name__ == "__main__":
    main()
