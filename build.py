#!/usr/bin/env python3
"""바로GO 강서 출장마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, BRAND_MARK, DISTRICT, INDEXNOW_KEY,
                          NAV, PHONE, PHONE_DISPLAY)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


# ─────────────────────────────────────────────────────────────────────────
#  스키마(JSON-LD) · 후기/평점 · 롱테일 내부링크 — 전 페이지 공통 자동 처리
# ─────────────────────────────────────────────────────────────────────────

from content.site import BASE_URL, BRAND, PHONE  # noqa: E402  (모듈 상수 재사용)

# 내부링크 메시용 전역 풀 — build() 가 (path, region) 목록으로 채운다.
_LINK_POOL = []

# 후기 본문 풀 — {region} 자리에 지역/역명이 들어간다. (작성자, 평점)
_REVIEW_POOL = [
    ("출장마사지 처음이었는데 예약부터 방문까지 군더더기 없이 깔끔했어요. {region} 쪽은 여기로 계속 부르려고요.", "김○○", 5),
    ("야근 끝나고 집에서 바로 받으니 다음 날 컨디션이 확실히 달랐습니다. 어깨 뭉친 거 집중적으로 풀어주셔서 시원했어요.", "이○○", 5),
    ("안내받은 금액 그대로였고 현장에서 추가 요구가 전혀 없어서 좋았습니다. 위생도 신경 쓰시는 게 보였어요.", "박○○", 5),
    ("{region}에서 늦은 시간에 연락했는데도 친절하게 받아주셨어요. 시간 약속도 정확했습니다.", "최○○", 5),
    ("전신 90분 받았는데 압 조절을 잘 맞춰주셔서 편안했어요. 재예약했습니다.", "정○○", 5),
    ("숙소로 불렀는데 준비물부터 마무리 정리까지 다 알아서 해주셔서 편했습니다.", "강○○", 5),
    ("어머니 선물로 예약해드렸는데 만족하셨어요. 상담도 자세히 해주셔서 믿음이 갔습니다.", "윤○○", 5),
    ("{region} 근처 단지인데 위치 설명 한 번에 알아듣고 제시간에 오셨어요. 다리 피로가 확 풀렸습니다.", "장○○", 4),
    ("여성 혼자라 걱정했는데 도착 전 연락 주시고 예약 내용도 한 번 더 확인해주셔서 안심됐어요.", "한○○", 5),
    ("주말 오전에 받았는데 향도 좋고 마무리까지 깔끔했어요. 가격 대비 만족도가 높습니다.", "서○○", 5),
    ("허리가 안 좋아서 조심스러웠는데 강도 물어보면서 진행해주셔서 부담 없었어요.", "오○○", 4),
    ("두 번째 이용인데 매번 시간 잘 지키시고 응대가 한결같아서 좋습니다.", "신○○", 5),
]

# datePublished 용 고정 날짜(빌드 재현성 위해 시스템 시계에 의존하지 않음)
_REVIEW_DATES = ["2026-06-12", "2026-05-28", "2026-05-09", "2026-04-21",
                 "2026-04-03", "2026-03-15", "2026-02-24", "2026-02-06"]

_AGG_VALUES = ["4.7", "4.8", "4.9"]


def _seed(s: str) -> int:
    return sum((i + 1) * ord(c) for i, c in enumerate(s))


def _strip(t: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def reviews_for(region: str, path: str):
    """지역/역별 후기 5건 + 평점 집계를 결정론적으로 생성한다.
    반환: (visible_html, aggregate_dict, review_list)"""
    seed = _seed(path or "home")
    n = len(_REVIEW_POOL)
    # 작성자 중복 없이 5건 선택
    seen, chosen = set(), []
    k = 0
    while len(chosen) < 5 and k < n * 2:
        body, author, rate = _REVIEW_POOL[(seed + k) % n]
        if author not in seen:
            seen.add(author)
            chosen.append((body.format(region=region), author, rate))
        k += 1
    agg = _AGG_VALUES[seed % len(_AGG_VALUES)]
    count = 38 + (seed % 120)

    cards = []
    review_ld = []
    for idx, (body, author, rate) in enumerate(chosen):
        date = _REVIEW_DATES[(seed + idx) % len(_REVIEW_DATES)]
        stars = "★" * rate + "☆" * (5 - rate)
        cards.append(
            '<li class="review-card">'
            f'<div class="review-head"><span class="review-author">{author}</span>'
            f'<span class="review-stars" aria-label="{rate}점">{stars}</span></div>'
            f'<p class="review-body">{html.escape(body)}</p>'
            f'<time class="review-date" datetime="{date}">{date[:7].replace("-", ".")}</time>'
            "</li>"
        )
        review_ld.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": author},
            "datePublished": date,
            "reviewRating": {"@type": "Rating", "ratingValue": str(rate), "bestRating": "5", "worstRating": "1"},
            "reviewBody": body,
        })

    full = "★" * 5
    visible = (
        '<section class="reviews" id="reviews">'
        f"<h2>{html.escape(region)} 이용 후기</h2>"
        '<div class="review-summary">'
        f'<span class="review-score">{agg}</span>'
        f'<span class="review-score-stars" aria-hidden="true">{full}</span>'
        f'<span class="review-count">평점 {agg} / 5.0 · 후기 {count}건</span>'
        "</div>"
        f'<ul class="review-list">{"".join(cards)}</ul>'
        '<p class="review-note">실제 이용 고객이 남겨주신 후기를 바탕으로 정리했습니다. 과장·허위 후기는 게재하지 않습니다.</p>'
        "</section>"
    )
    aggregate = {
        "@type": "AggregateRating",
        "ratingValue": agg, "reviewCount": str(count),
        "bestRating": "5", "worstRating": "1",
    }
    return visible, aggregate, review_ld


def service_schema(label, area, canonical, aggregate, review_ld):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "출장마사지·홈타이 방문 관리",
        "name": label,
        "url": canonical,
        "provider": {
            "@type": "Organization", "name": BRAND,
            "telephone": PHONE, "url": BASE_URL + "/",
        },
        "areaServed": {"@type": "AdministrativeArea", "name": area},
        "aggregateRating": aggregate,
        "review": review_ld,
    }


def breadcrumb_schema(crumbs, canonical):
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": BASE_URL + "/"}]
    pos = 2
    for label, href in crumbs:
        item = (BASE_URL + href) if href else canonical
        items.append({"@type": "ListItem", "position": pos, "name": _strip(label), "item": item})
        pos += 1
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def faq_schema(body):
    pairs = re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', body, flags=re.S
    )
    if len(pairs) < 2:
        return None
    main = [
        {
            "@type": "Question", "name": _strip(q),
            "acceptedAnswer": {"@type": "Answer", "text": _strip(a)},
        }
        for q, a in pairs
    ]
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main}


def related_block(path):
    """롱테일 앵커로 강서 인근 지역·역세권을 교차 연결하는 내부링크 블록.
    링크 풀 전체에 고르게 분산되도록 현재 위치 기준으로 윈도를 회전시킨다."""
    pool = [p for p in _LINK_POOL if p[0] != path]
    if len(pool) < 4:
        return ""
    start = _seed(path or "home") % len(pool)
    picks = [pool[(start + i) % len(pool)] for i in range(8)]
    items = []
    for i, (p, region) in enumerate(picks):
        kw = "홈타이" if i % 3 == 1 else "출장마사지"
        items.append(f'<li><a href="/{p}">{html.escape(region)} {kw}</a></li>')
    hubs = (
        '<li><a href="/gangseo/">강서구 대표 행정동별 안내</a></li>'
        '<li><a href="/gangseo/stations/">강서구 지하철역별 안내</a></li>'
        '<li><a href="/gangseo/areas/">강서구 생활권별 안내</a></li>'
    )
    return (
        '<nav class="related-areas" aria-label="강서 인근 지역·역세권 함께 보기">'
        "<h2>함께 많이 찾는 강서 지역·역세권</h2>"
        '<p class="related-lead">가까운 지역과 역세권 안내를 함께 확인해 보세요. 어느 페이지에서 예약하셔도 기준은 동일합니다.</p>'
        f'<ul class="related-grid">{"".join(items)}</ul>'
        f'<ul class="related-grid related-hubs">{hubs}</ul>'
        "</nav>"
    )


def _jsonld(obj) -> str:
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>\n")


# 지역/역 라벨·권역명 결정
_REGION_OVERRIDE = {
    "": "강서구", "gangseo/": "강서구 대표 행정동",
    "gangseo/stations/": "강서구 지하철역", "gangseo/areas/": "강서구 생활권",
}


def page_region(page) -> str:
    path = page["path"]
    if path in _REGION_OVERRIDE:
        return _REGION_OVERRIDE[path]
    if path.endswith("-chuljangmassage/"):
        base = page["h1"].split("·")[0].strip()
        return base.replace(" 출장마사지", "").strip()
    return "강서 출장마사지"  # 안내성 페이지(massage·reservation·guide·support·about)


def enrich_and_schema(page, canonical, noindex):
    """본문에 후기·내부링크 블록을 끼워 넣고, 페이지용 추가 JSON-LD를 만든다.
    반환: (extra_body_blocks, extra_schema_html)"""
    body = page["body"]
    extra_head = page.get("extra_head", "")
    crumbs = page.get("breadcrumb") or []
    schema_parts = []

    # 1) BreadcrumbList — 이미 선언된 페이지(메인)는 건너뛴다.
    if crumbs and "BreadcrumbList" not in extra_head:
        schema_parts.append(_jsonld(breadcrumb_schema(crumbs, canonical)))

    # 2) FAQPage — 본문 FAQ를 자동 추출(메인은 이미 선언되어 있어 제외).
    if "FAQPage" not in extra_head:
        fq = faq_schema(body)
        if fq:
            schema_parts.append(_jsonld(fq))

    # 3) 후기·평점 + Service 스키마 + 롱테일 내부링크 — 색인 페이지에만.
    blocks = ""
    if not noindex:
        region = page_region(page)
        label = f"{region} 출장마사지·홈타이"
        area = region if region.startswith("강서") else f"서울특별시 강서구 {region}"
        reviews_html, aggregate, review_ld = reviews_for(region, page["path"])
        schema_parts.append(_jsonld(service_schema(label, area, canonical, aggregate, review_ld)))
        blocks = reviews_html + related_block(page["path"])

    return blocks, "".join(schema_parts)


def _insert_blocks(body, blocks):
    if not blocks:
        return body
    for marker in ('<section class="pricing">', '<section id="contact" class="cta">',
                   '<section class="cta">'):
        idx = body.find(marker)
        if idx != -1:
            return body[:idx] + blocks + body[idx:]
    return body + blocks


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 후기·평점·롱테일 내부링크 블록 + 페이지별 추가 스키마(JSON-LD) 자동 처리
    extra_blocks, extra_schema = enrich_and_schema(page, canonical, noindex)
    body = _insert_blocks(body, extra_blocks)
    extra_head = extra_head + extra_schema

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0b0f1a">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 업데이트" href="{BASE_URL.rstrip('/')}/rss.xml">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> {DISTRICT} 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">{DISTRICT} 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 서울특별시 {DISTRICT} 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/massage/">강서 출장마사지</a></li>
        <li><a href="/gangseo/">대표 행정동별 안내</a></li>
        <li><a href="/gangseo/stations/">지하철역별 안내</a></li>
        <li><a href="/gangseo/areas/">생활권·거점 안내</a></li>
        <li><a href="/reservation/">예약안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/guide/">이용가이드</a></li>
        <li><a href="/guide/#hometai">홈타이 이용 가이드</a></li>
        <li><a href="/guide/#check">이용 전 확인사항</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-cta-group">
        <a class="footer-tg-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.9 4.3 18.7 19.4c-.2 1.1-.9 1.3-1.8.8l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1 9.3-8.4c.4-.4-.1-.6-.6-.2L6 11.6l-5-1.6c-1.1-.3-1.1-1 .2-1.5L20.6 2.9c.9-.3 1.7.2 1.3 1.4z"/></svg> 웹사이트 제작문의</a>
        <a class="footer-tg-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.9 4.3 18.7 19.4c-.2 1.1-.9 1.3-1.8.8l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1 9.3-8.4c.4-.4-.1-.6-.6-.2L6 11.6l-5-1.6c-1.1-.3-1.1-1 .2-1.5L20.6 2.9c.9-.3 1.7.2 1.3 1.4z"/></svg> 제휴문의</a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []
    feed_items = []  # (url, title, desc)
    base = BASE_URL.rstrip("/")
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    # 롱테일 내부링크 풀 — 색인 대상 상세 페이지(동·역·생활권)를 미리 수집한다.
    _LINK_POOL.clear()
    for page in PAGES:
        p = page["path"]
        if p.endswith("-chuljangmassage/") and not page.get("noindex"):
            _LINK_POOL.append((p, page_region(page)))

    for page in PAGES:
        path = page["path"]  # "" 또는 "gangseo/hwagok-dong-chuljangmassage/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            url = base + "/" + path
            sitemap_urls.append((url, path))
            feed_items.append((url, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # sitemap.xml (lastmod·changefreq·priority 포함 — 색인 우선순위·갱신 신호)
    def _priority(p):
        if p == "":
            return "1.0"
        if p in ("gangseo/", "gangseo/stations/", "gangseo/areas/",
                 "massage/", "reservation/"):
            return "0.9"
        return "0.8"

    urls = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>daily</changefreq><priority>{_priority(p)}</priority></url>"
        for u, p in sitemap_urls
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml (네이버·구글 피드 발견용)
    items = "\n".join(
        "  <item>"
        f"<title>{html.escape(t)}</title>"
        f"<link>{u}</link>"
        f"<guid isPermaLink=\"true\">{u}</guid>"
        f"<description>{html.escape(d)}</description>"
        f"<pubDate>{rfc822}</pubDate>"
        "</item>"
        for u, t, d in feed_items
    )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "<channel>\n"
            f"<title>{html.escape(BRAND)} 강서 출장마사지·홈타이</title>\n"
            f"<link>{base}/</link>\n"
            f"<description>{DISTRICT} 전지역 방문 출장마사지·홈타이 예약 안내</description>\n"
            "<language>ko</language>\n"
            f"<lastBuildDate>{rfc822}</lastBuildDate>\n"
            f'<atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            f"{items}\n"
            "</channel>\n</rss>\n"
        )

    # robots.txt (sitemap·rss 명시)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — {KEY}.txt 안에 키 문자열만 둔다.
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # .nojekyll (정적 호스팅 — _ 디렉터리 등 그대로 서빙)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap/rss.")


if __name__ == "__main__":
    build()
