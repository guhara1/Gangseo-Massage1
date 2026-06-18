# 바로GO 강서 출장마사지 — 지역 SEO 사이트

서울 강서구 방문형 출장마사지·홈타이 안내 사이트. `content/` 페이지 정의를 읽어
`build.py`가 정적 HTML을 생성한다.

## 빌드

```bash
python3 build.py
```

페이지별 글자수 리포트가 출력되며, 2,000자 미만 페이지는 자동 noindex 처리되고
`sitemap.xml`·`robots.txt`·`.nojekyll`이 함께 생성된다.

## 구조

```
build.py              빌드 스크립트 — 레이아웃·TOC·글자수 검사·sitemap
content/
  site.py             BASE_URL·상호(바로GO)·전화·메뉴(NAV)
  main.py             메인(/) — Organization/WebPage/BreadcrumbList/FAQPage JSON-LD, 히어로
  _helpers.py         make_dong / make_station / make_district + 공용 CTA
  pricing.py          공용 요금 블록
  areas.py            대표 행정동 허브(/gangseo/) + areas_data.py(동 8)
  stations.py         지하철역 허브(/gangseo/stations/) + stations_a/b.py(역 18)
  districts.py        생활권 허브(/gangseo/areas/) + districts_data.py(거점 10)
  info.py             강서 출장마사지 안내·예약·가이드·고객센터·약관
  about.py            운영자 소개 (E-E-A-T)
assets/
  style.css           프리미엄 다크 스파 — 토큰 팔레트 + 컴포넌트 오버레이, Pretendard 본문
  nav.js, favicon.*, og-image.png
```

## 페이지 구성

- 메인 1
- 대표 행정동 8 (염창·등촌·화곡·가양·발산·공항·방화·우장산) + 허브 1
- 지하철역 18 (5·9호선·공항철도·김포골드라인) + 허브 1
- 생활권·거점 10 (마곡지구·김포공항 인근 등) + 허브 1
- 안내 페이지 (강서 출장마사지·예약·가이드·고객센터·운영자 소개) + 약관 2(noindex)

## SEO 원칙

- 번호 행정동(화곡1동 등)은 대표 동으로 통합, 단독 페이지 금지
- 환승역(김포공항역·마곡나루역·까치산역)은 역명당 URL 하나, 노선별 분리 금지
- 본문 2,000~2,500자, 디스크립션 80자 이하, 페이지 간 유사도 최소화
- 오프라인 사업장 주소가 없는 방문형이므로 LocalBusiness 대신 Organization 스키마 사용

## 배포 전 확인

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경 후 재빌드
2. `python3 build.py` 경고(⚠) 0건 확인
3. Search Console / 네이버 서치어드바이저에 `sitemap.xml` 제출
