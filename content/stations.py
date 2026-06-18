# 지하철역·공항철도역별 안내 — 허브 1개 + 역 18개.
# 환승역도 노선별로 쪼개지 않고 역명당 URL 하나만 사용한다.
from ._helpers import CTA
from .pricing import PRICING
from .stations_a import STATIONS_A
from .stations_b import STATIONS_B

_HUB_BODY = """
<p class="lead">강서구를 지나는 5호선·9호선·공항철도·김포골드라인 주요 역세권을 기준으로 방문 관리를 안내합니다. 환승역은 노선이 여러 개라도 역명당 페이지는 하나만 운영합니다.</p>

<section>
<h2>역세권 안내 구성 기준</h2>
<p>강서구는 서울 서부 교통의 관문으로 여러 노선이 지나갑니다. 이 사이트의 역 안내는 역마다 페이지 하나를 두는 단일 페이지 원칙을 따릅니다. 김포공항역처럼 5호선·9호선·공항철도·김포골드라인·서해선이 모이는 거대 환승역도, 마곡나루역이나 까치산역처럼 두 노선이 겹치는 역도 페이지는 하나입니다. 출구 번호별 페이지나 역 이름에 관리 코스를 붙인 조합 페이지, 노선별·방향별 중복 URL은 만들지 않습니다. 그런 페이지는 내용이 겹칠 수밖에 없고 검색 이용자에게도 도움이 되지 않기 때문입니다. 각 역 페이지에서는 역세권 분위기, 인근 대표 동, 방문 형태, 예약 시 참고사항을 역마다 고유하게 설명합니다.</p>
</section>

<section>
<h2>5호선 강서권</h2>
<p>5호선은 강서구 서부와 중부를 지납니다. 서쪽 종점 <a href="/gangseo/banghwa-station-chuljangmassage/">방화역</a>부터 <a href="/gangseo/gaehwasan-station-chuljangmassage/">개화산역</a>, <a href="/gangseo/gonghang-market-station-chuljangmassage/">공항시장역</a>, <a href="/gangseo/songjeong-station-chuljangmassage/">송정역</a>, <a href="/gangseo/gimpo-airport-station-chuljangmassage/">김포공항역</a>, <a href="/gangseo/magok-station-chuljangmassage/">마곡역</a>, <a href="/gangseo/balsan-station-chuljangmassage/">발산역</a>, <a href="/gangseo/ujangsan-station-chuljangmassage/">우장산역</a>, <a href="/gangseo/hwagok-station-chuljangmassage/">화곡역</a>, 2호선 지선과 만나는 <a href="/gangseo/kkachisan-station-chuljangmassage/">까치산역</a>까지 이어집니다. 공항권·업무권·주거권을 모두 통과하는 노선입니다.</p>
</section>

<section>
<h2>9호선 강서권</h2>
<p>9호선은 강서구 한강변을 따라 동서로 지납니다. <a href="/gangseo/gaehwa-station-chuljangmassage/">개화역</a>(김포골드라인)·김포공항역 방면에서 시작해 <a href="/gangseo/sinbanghwa-station-chuljangmassage/">신방화역</a>, <a href="/gangseo/magongnaru-station-chuljangmassage/">마곡나루역</a>, <a href="/gangseo/yangcheon-hyanggyo-station-chuljangmassage/">양천향교역</a>, <a href="/gangseo/gayang-station-chuljangmassage/">가양역</a>, <a href="/gangseo/jeungmi-station-chuljangmassage/">증미역</a>, <a href="/gangseo/deungchon-station-chuljangmassage/">등촌역</a>, <a href="/gangseo/yeomchang-station-chuljangmassage/">염창역</a>으로 이어집니다. 마곡지구와 가양·등촌·염창 한강변 생활권을 연결하는 노선입니다.</p>
</section>

<section>
<h2>환승역과 공항철도</h2>
<p>김포공항역은 5호선·9호선·공항철도·김포골드라인·서해선이 모두 만나는 강서구 최대 환승역이지만, 노선을 나누지 않고 역명 기준 한 페이지로 안내합니다. 마곡나루역은 9호선과 공항철도가 만나는 환승역이고, 까치산역은 2호선 지선과 5호선이 만나는 환승역입니다. 모두 역명당 하나의 페이지로만 운영하며, GTX·서부광역철도 같은 미확정 노선이나 운행 전 예정역은 단독 페이지로 만들지 않고 본문 보조 설명으로만 다룹니다.</p>
</section>

<section>
<h2>역세권별 분위기 한눈에 보기</h2>
<p>열여덟 개 역은 성격이 뚜렷하게 갈립니다. 김포공항역과 송정역, 공항시장역은 공항 배후 상권형이라 출장·숙박 방문과 심야 문의가 많고, 마곡나루역과 마곡역, 발산역은 업무·연구 단지형이라 야근 후 평일 저녁 예약이 중심입니다. 화곡역과 까치산역, 우장산역은 주거 밀집 역세권이라 가족 단위 자택 예약이 많습니다. 가양역·증미역·등촌역·염창역·양천향교역은 9호선 한강변 생활권으로 대단지 아파트 방문이 주를 이루고, 방화역·개화산역·신방화역·개화역은 강서구 서부 끝의 한적한 주거 역세권입니다. 본인 생활 패턴과 비슷한 역 페이지를 골라 보시면 필요한 정보가 더 빨리 보입니다. 두 역 사이 애매한 위치라면 둘 중 어느 페이지를 보셔도 되고, 최종 안내는 언제나 도로명 주소 기준으로 이루어집니다. 버스 정류장이나 큰 사거리를 기준으로 설명하셔도 예약에는 전혀 문제가 없습니다.</p>
</section>

<section>
<h2>역 기준으로 예약하실 때</h2>
<p>역 이름은 위치를 설명하는 좋은 기준이지만, 실제 방문에는 정확한 도로명 주소가 필요합니다. 예약 전화에서 가까운 역과 함께 건물명 또는 도로명 주소를 알려주시면 도착 시간을 정확히 안내해 드립니다. 거주 지역 기준이 편하시면 <a href="/gangseo/">대표 행정동별 안내</a>를, 거점 기준이 궁금하시면 <a href="/gangseo/areas/">생활권·주요 거점별 안내</a>를 확인해 주세요. 어느 역에서 출발하든 예약 절차와 이용 기준은 동일하며, 역과 코스를 조합한 별도 페이지는 운영하지 않습니다.</p>
</section>

<section>
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>역에서 만나서 같이 이동하는 방식인가요?</h3>
<p>아니요, 관리사가 장비를 챙겨 알려주신 주소로 직접 방문합니다. 역은 위치를 설명하는 기준일 뿐 만남 장소가 아닙니다.</p>
</div>
<div class="faq-item">
<h3>김포공항역은 노선이 많은데 무슨 호선인지 말해야 하나요?</h3>
<p>노선 구분은 필요 없습니다. 환승역 페이지는 역명 기준 하나로 통합되어 있고, 방문은 도로명 주소 기준으로 진행됩니다.</p>
</div>
<div class="faq-item">
<h3>역에서 먼 곳은 안 되나요?</h3>
<p>역과의 거리는 가능 여부와 무관합니다. 강서구 전지역이 방문 범위이며, 역 페이지는 위치 설명을 돕는 안내일 뿐입니다.</p>
</div>
</section>
""" + PRICING + CTA

HUB = {
    "path": "gangseo/stations/",
    "title": "강서 지하철역 출장마사지｜역세권 방문 관리 안내",
    "desc": "강서구 지하철역·공항철도역 출장마사지·홈타이 역세권 방문 안내입니다.",
    "h1": "강서구 지하철역별 안내",
    "body": _HUB_BODY,
    "breadcrumb": [("지하철역별 안내", None)],
}

PAGES = [HUB] + STATIONS_A + STATIONS_B
