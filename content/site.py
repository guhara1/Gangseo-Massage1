# 사이트 공통 설정 — 강서 출장마사지 (바로GO)
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://gangseo-massage1.pages.dev"

BRAND = "바로GO"
BRAND_MARK = "바"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"
DISTRICT = "강서구"
REGION_LEAD = "강서구 전지역 방문 관리"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("강서 출장마사지", "/massage/", [
        ("출장마사지 안내", "/massage/#service"),
        ("홈타이 안내", "/massage/#hometai"),
        ("전지역 방문 안내", "/massage/#coverage"),
        ("예약 가능 시간", "/massage/#hours"),
        ("이용 전 확인사항", "/massage/#check"),
        ("위생·안전 안내", "/massage/#safety"),
        ("자주 묻는 질문", "/massage/#faq"),
    ]),
    ("지역별 안내", "/gangseo/", [
        ("강서구 전체", "/gangseo/"),
        ("염창동", "/gangseo/yeomchang-dong-chuljangmassage/"),
        ("등촌동", "/gangseo/deungchon-dong-chuljangmassage/"),
        ("화곡동", "/gangseo/hwagok-dong-chuljangmassage/"),
        ("가양동", "/gangseo/gayang-dong-chuljangmassage/"),
        ("발산동", "/gangseo/balsan-dong-chuljangmassage/"),
        ("공항동", "/gangseo/gonghang-dong-chuljangmassage/"),
        ("방화동", "/gangseo/banghwa-dong-chuljangmassage/"),
        ("우장산동", "/gangseo/ujangsan-dong-chuljangmassage/"),
    ]),
    ("지하철역별 안내", "/gangseo/stations/", [
        ("역 전체", "/gangseo/stations/"),
        ("김포공항역", "/gangseo/gimpo-airport-station-chuljangmassage/"),
        ("마곡나루역", "/gangseo/magongnaru-station-chuljangmassage/"),
        ("마곡역", "/gangseo/magok-station-chuljangmassage/"),
        ("발산역", "/gangseo/balsan-station-chuljangmassage/"),
        ("우장산역", "/gangseo/ujangsan-station-chuljangmassage/"),
        ("화곡역", "/gangseo/hwagok-station-chuljangmassage/"),
        ("까치산역", "/gangseo/kkachisan-station-chuljangmassage/"),
        ("가양역", "/gangseo/gayang-station-chuljangmassage/"),
        ("등촌역", "/gangseo/deungchon-station-chuljangmassage/"),
        ("염창역", "/gangseo/yeomchang-station-chuljangmassage/"),
    ]),
    ("생활권 안내", "/gangseo/areas/", [
        ("생활권 전체", "/gangseo/areas/"),
        ("마곡지구", "/gangseo/magok-district-chuljangmassage/"),
        ("김포공항 인근", "/gangseo/gimpo-airport-area-chuljangmassage/"),
        ("발산역 생활권", "/gangseo/balsan-area-chuljangmassage/"),
        ("화곡역 생활권", "/gangseo/hwagok-area-chuljangmassage/"),
        ("까치산역 생활권", "/gangseo/kkachisan-area-chuljangmassage/"),
        ("등촌역 생활권", "/gangseo/deungchon-area-chuljangmassage/"),
        ("가양역 생활권", "/gangseo/gayang-area-chuljangmassage/"),
        ("염창동 한강변", "/gangseo/yeomchang-hangang-area-chuljangmassage/"),
        ("방화동·개화산", "/gangseo/banghwa-gaehwasan-area-chuljangmassage/"),
        ("우장산공원 인근", "/gangseo/ujangsan-park-area-chuljangmassage/"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("홈타이 이용 가이드", "/guide/#hometai"),
        ("이용 전 확인사항", "/guide/#check"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("운영자 소개", "/about/"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
