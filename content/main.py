# 메인 페이지 — 강서구 허브. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
# 방문형(오프라인 주소 없음) 사이트이므로 LocalBusiness 대신 Organization 스키마 사용.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<meta name="naver-site-verification" content="ffe6710ee053c00045f6c87c97f92ee7861cb578" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "alternateName": "바로GO 강서 출장마사지",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "logo": "{BASE_URL}/assets/icon-512.png",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "강서구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 강서구"
  }},
  "contactPoint": {{
    "@type": "ContactPoint",
    "telephone": "{PHONE}",
    "contactType": "reservations",
    "areaServed": "KR",
    "availableLanguage": "Korean"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "강서 출장마사지·강서구 홈타이 지역별 예약 안내",
  "url": "{BASE_URL}/",
  "primaryImageOfPage": "{BASE_URL}/assets/og-image.png",
  "isPartOf": {{ "@type": "WebSite", "name": "{BRAND}", "url": "{BASE_URL}/" }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "홈", "item": "{BASE_URL}/" }}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "강서구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 달라집니다. 염창동, 등촌동, 화곡동, 가양동, 발산동, 공항동, 방화동, 우장산동 대표 행정동 기준으로 지역별 안내에서 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "김포공항역이나 마곡나루역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 환승역도 노선별로 나누지 않고 역명 기준 하나의 페이지로 안내하며, 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "화곡1동, 화곡2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "화곡본동과 화곡1·2·3·4·6·8동은 화곡동 대표 페이지에서 통합 안내합니다. 같은 생활권을 지역명만 바꿔 반복하는 페이지를 만들지 않기 위함입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "홈타이와 출장마사지는 어떻게 다른가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "강서 홈타이는 자택·숙소·사무실 인근에서 받는 방문형 관리 서비스로, 출장마사지와 같은 방문 관리의 한 형태입니다. 코스와 기법에 따라 구분되며 예약 절차는 동일합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "당일 예약도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "가능할 수 있지만 저녁 시간대와 주말, 김포공항 인근 심야 시간대는 문의가 몰릴 수 있어 사전 예약을 권장합니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 강서구 전지역</p>
    <h1>강서 출장마사지·강서구 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>마곡·발산·화곡·김포공항 생활권 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/reservation/">예약 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>8개</strong><span>대표 행정동</span></li>
      <li><strong>18개</strong><span>역세권 안내</span></li>
      <li><strong>10개</strong><span>생활권 거점</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="why">
<h2>강서구에서 출장마사지를 찾는 이유</h2>
<p>강서 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 강서구는 서울 서쪽 끝의 자치구로 김포공항과 마곡지구, 발산역 상권, 화곡동 주거지, 등촌·가양 한강변 생활권, 방화동·개화산 생활권이 한 구 안에 모여 있습니다. 같은 강서구라도 생활권마다 이동 거리와 분위기가 크게 달라, 이 사이트는 "강서 전지역 가능"이라고만 적는 대신 대표 행정동·역세권·생활권을 나눠 안내합니다. 이 페이지는 강서구 전체 구조를 설명하는 허브이며, 상세 내용은 각 안내 페이지에서 확인하실 수 있습니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차로 진행합니다.</p>
</section>

<section id="coverage">
<h2>대표 행정동별 방문 가능 지역 안내</h2>
<p>강서구 지역 안내는 염창동, 등촌동, 화곡동, 가양동, 발산동, 공항동, 방화동, 우장산동 여덟 개 대표 행정동을 중심으로 구성합니다. 화곡본동부터 화곡8동, 등촌1~3동, 가양1~3동, 방화1~3동처럼 번호로 나뉜 행정동은 별도 페이지를 만들지 않고 각 대표 동 페이지에서 통합 안내합니다. 지역명만 바꾼 반복 페이지는 검색 품질에도 도움이 되지 않기 때문입니다.</p>
<ul class="card-grid">
<li><a href="/gangseo/yeomchang-dong-chuljangmassage/">염창동</a></li>
<li><a href="/gangseo/deungchon-dong-chuljangmassage/">등촌동</a></li>
<li><a href="/gangseo/hwagok-dong-chuljangmassage/">화곡동</a></li>
<li><a href="/gangseo/gayang-dong-chuljangmassage/">가양동</a></li>
<li><a href="/gangseo/balsan-dong-chuljangmassage/">발산동</a></li>
<li><a href="/gangseo/gonghang-dong-chuljangmassage/">공항동</a></li>
<li><a href="/gangseo/banghwa-dong-chuljangmassage/">방화동</a></li>
<li><a href="/gangseo/ujangsan-dong-chuljangmassage/">우장산동</a></li>
</ul>
<p>강서구 전체 구성이 궁금하시면 <a href="/gangseo/">대표 행정동별 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>김포공항역·마곡나루역·발산역·화곡역 역세권 안내</h2>
<p>강서구는 5호선·9호선·공항철도가 지나는 교통 요지라 역 기준으로 위치를 설명하는 분이 많습니다. 지하철역별 안내는 김포공항역, 마곡나루역, 발산역, 화곡역, 까치산역처럼 실제 검색 수요가 있는 역을 기준으로 구성하며, 환승역도 노선별로 쪼개지 않고 역명당 한 페이지만 운영합니다. 출구별 페이지나 역과 코스를 조합한 페이지는 만들지 않습니다.</p>
<ul class="card-grid">
<li><a href="/gangseo/gimpo-airport-station-chuljangmassage/">김포공항역</a></li>
<li><a href="/gangseo/magongnaru-station-chuljangmassage/">마곡나루역</a></li>
<li><a href="/gangseo/magok-station-chuljangmassage/">마곡역</a></li>
<li><a href="/gangseo/balsan-station-chuljangmassage/">발산역</a></li>
<li><a href="/gangseo/ujangsan-station-chuljangmassage/">우장산역</a></li>
<li><a href="/gangseo/hwagok-station-chuljangmassage/">화곡역</a></li>
<li><a href="/gangseo/kkachisan-station-chuljangmassage/">까치산역</a></li>
<li><a href="/gangseo/gayang-station-chuljangmassage/">가양역</a></li>
<li><a href="/gangseo/deungchon-station-chuljangmassage/">등촌역</a></li>
<li><a href="/gangseo/yeomchang-station-chuljangmassage/">염창역</a></li>
</ul>
<p>방화역, 개화산역, 송정역, 공항시장역, 신방화역, 양천향교역, 증미역, 개화역을 포함한 전체 목록은 <a href="/gangseo/stations/">지하철역별 안내</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="districts">
<h2>마곡·발산·화곡·등촌·방화 생활권 차이</h2>
<p>강서구는 같은 구 안에서도 생활권의 성격이 뚜렷하게 갈립니다. 마곡지구는 업무·연구 단지와 신축 오피스텔이 모인 생활권이고, 김포공항 인근은 공항 이용객과 인근 숙박 수요가 있는 지역입니다. 발산역 생활권은 병원·업무·주거가 섞여 있고, 화곡역과 까치산역 생활권은 강서구에서 가장 넓은 주거권입니다. 등촌·가양·염창 한강변 생활권은 아파트 단지와 한강공원이 가깝고, 방화동·개화산 생활권은 서부 끝의 한적한 주거지입니다.</p>
<ul class="card-grid">
<li><a href="/gangseo/magok-district-chuljangmassage/">마곡지구</a></li>
<li><a href="/gangseo/gimpo-airport-area-chuljangmassage/">김포공항 인근</a></li>
<li><a href="/gangseo/balsan-area-chuljangmassage/">발산역 생활권</a></li>
<li><a href="/gangseo/hwagok-area-chuljangmassage/">화곡역 생활권</a></li>
<li><a href="/gangseo/kkachisan-area-chuljangmassage/">까치산역 생활권</a></li>
<li><a href="/gangseo/deungchon-area-chuljangmassage/">등촌역 생활권</a></li>
<li><a href="/gangseo/gayang-area-chuljangmassage/">가양역 생활권</a></li>
<li><a href="/gangseo/yeomchang-hangang-area-chuljangmassage/">염창동 한강변</a></li>
<li><a href="/gangseo/banghwa-gaehwasan-area-chuljangmassage/">방화동·개화산</a></li>
<li><a href="/gangseo/ujangsan-park-area-chuljangmassage/">우장산공원 인근</a></li>
</ul>
</section>

<section id="hometai">
<h2>강서 홈타이 예약 전 확인사항</h2>
<p>강서 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비 여부, 결제 방식, 취소 기준, 서비스 범위를 먼저 확인하시는 것이 좋습니다. 강서구는 같은 구 안에서도 염창·등촌 한강변, 화곡 주거권, 마곡·발산 업무권, 김포공항·방화 서부권의 이동 기준이 다르며, 특히 김포공항·개화동·방화동 일부는 차량 이동 시간이 달라질 수 있어 예약 가능 시간과 추가 이동비 여부를 명확히 안내해 드립니다. 자세한 준비사항은 <a href="/reservation/">예약안내</a>와 <a href="/guide/">이용가이드</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="check">
<h2>이용 전 확인사항</h2>
<p>원활한 방문 관리를 위해 정확한 도로명 주소, 공동현관 출입 방법, 주차 가능 여부, 조용한 공간 확보 여부를 미리 확인해 주시면 좋습니다. 마곡지구나 가양·염창 한강변의 오피스텔·아파트는 방문 차량 등록과 공동현관 호출 방식을, 김포공항 인근 숙박시설은 호실과 프런트 경유 여부를 함께 알려주세요. 강서구는 끝과 끝의 이동 시간이 꽤 차이 나므로, 시간 약속이 중요한 일정이라면 한두 시간 여유를 두고 예약하시기를 권장합니다.</p>
</section>

<section id="safety">
<h2>위생 및 안전 안내</h2>
<p>건전하고 안전한 방문 관리를 위해 위생 기준, 예약 정보 확인, 개인정보 보호, 금지행위 안내를 명확히 제공합니다. 과장된 표현이나 허위 후기, 선정적인 문구는 사용하지 않으며, 불법적이거나 무리한 요청은 어떤 경우에도 진행하지 않는다는 기준을 분명히 안내드립니다. 예약 정보는 관리 목적 외에 사용하지 않습니다. 운영 주체와 콘텐츠 작성 기준은 <a href="/about/">운영자 소개</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="guide">
<h2>강서 출장마사지 사이트 이용 가이드</h2>
<p>메인페이지는 강서구 전체 안내를 담당하고, 대표 행정동 페이지는 염창동·등촌동·화곡동·가양동·발산동·공항동·방화동·우장산동 검색을, 역세권 페이지는 김포공항역·마곡나루역·발산역·화곡역·까치산역 등 실제 검색 수요가 있는 역을 담당합니다. 생활권 페이지는 마곡지구나 김포공항 인근처럼 거점 단위로 정리했습니다. 거주 지역 기준이 편하시면 <a href="/gangseo/">지역별 안내</a>를, 역 기준이 익숙하시면 <a href="/gangseo/stations/">지하철역별 안내</a>를, 거점 기준은 <a href="/gangseo/areas/">생활권 안내</a>를 보시면 됩니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>강서구 전지역 방문이 가능한가요?</h3>
<p>예약 시간, 정확한 위치, 배정 상황에 따라 달라집니다. 염창동, 등촌동, 화곡동, 가양동, 발산동, 공항동, 방화동, 우장산동 대표 행정동 기준으로 <a href="/gangseo/">지역별 안내</a>에서 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>김포공항역이나 마곡나루역 근처도 가능한가요?</h3>
<p>주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 환승역도 노선별로 나누지 않고 역명 기준 하나의 페이지로 안내하며, 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>화곡1동, 화곡2동은 왜 따로 없나요?</h3>
<p>화곡본동과 화곡1·2·3·4·6·8동은 화곡동 대표 페이지에서 통합 안내합니다. 같은 생활권을 지역명만 바꿔 반복하는 페이지를 만들지 않기 위함입니다.</p>
</div>
<div class="faq-item">
<h3>홈타이와 출장마사지는 어떻게 다른가요?</h3>
<p>강서 홈타이는 자택·숙소·사무실 인근에서 받는 방문형 관리 서비스로, 출장마사지와 같은 방문 관리의 한 형태입니다. 코스와 기법에 따라 구분되며 예약 절차는 동일합니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말, 김포공항 인근 심야 시간대는 문의가 몰릴 수 있어 사전 예약을 권장합니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>강서구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "강서 출장마사지｜강서구 홈타이 지역별 예약 안내",
    "desc": "강서 출장마사지·홈타이 예약 전 행정동, 역세권, 이용 기준을 정리했습니다.",
    "h1": "강서 출장마사지·강서구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
