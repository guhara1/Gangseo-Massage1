# 페이지 dict 생성 공용 헬퍼 — 지역/역/생활권 데이터 모듈이 공유한다.
from .site import PHONE, PHONE_DISPLAY
from .pricing import PRICING

CTA = f"""
<section class="cta">
<h2>예약문의</h2>
<p>방문 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""


def make_dong(slug, name, title, desc, body):
    """대표 행정동 페이지 — URL: /gangseo/{slug}-chuljangmassage/"""
    return {
        "path": f"gangseo/{slug}-chuljangmassage/",
        "title": title,
        "desc": desc,
        "h1": f"{name} 출장마사지·홈타이 안내",
        "body": body + PRICING + CTA,
        "breadcrumb": [("대표 행정동별 안내", "/gangseo/"), (name, None)],
    }


def make_station(slug, name, title, desc, body):
    """지하철역 페이지 — URL: /gangseo/{slug}-chuljangmassage/ (slug 끝에 -station)"""
    return {
        "path": f"gangseo/{slug}-chuljangmassage/",
        "title": title,
        "desc": desc,
        "h1": f"{name} 출장마사지·홈타이 인근 안내",
        "body": body + PRICING + CTA,
        "breadcrumb": [("지하철역별 안내", "/gangseo/stations/"), (name, None)],
    }


def make_district(slug, name, title, desc, body):
    """생활권·주요 거점 페이지 — URL: /gangseo/{slug}-chuljangmassage/"""
    return {
        "path": f"gangseo/{slug}-chuljangmassage/",
        "title": title,
        "desc": desc,
        "h1": f"{name} 출장마사지·홈타이 안내",
        "body": body + PRICING + CTA,
        "breadcrumb": [("생활권·주요 거점별 안내", "/gangseo/areas/"), (name, None)],
    }
