# 색인 통보 도구 (tools/)

빌드(`python build.py`)는 다음을 자동 생성한다.

| 파일 | 용도 |
|------|------|
| `sitemap.xml` | 색인 페이지 목록 + `<lastmod>` (구글·네이버·빙) |
| `rss.xml` | 피드 발견용 (네이버·구글) |
| `robots.txt` | `Sitemap:` 2줄(sitemap·rss) 명시 |
| `{INDEXNOW_KEY}.txt` | IndexNow 키 검증 파일 (사이트 루트) |
| `<head>` | `naver-site-verification`(메인), `rss+xml` alternate 링크 |

## 1. IndexNow — 빙·네이버·얀덱스 즉시 통보 (의존성 없음)

글을 새로 올리거나 페이지를 수정할 때마다 실행:

```bash
python build.py                 # 먼저 재빌드(sitemap 갱신)
python tools/indexnow.py        # sitemap 전체를 빙·네이버·얀덱스에 즉시 통보

# 특정 URL만 통보 (가장 빠름)
python tools/indexnow.py https://gangseo-massage1.pages.dev/gangseo/hwagok-dong-chuljangmassage/
```

- 키 파일 `https://gangseo-massage1.pages.dev/{KEY}.txt` 가 배포되어 있어야 검증된다(빌드가 자동 생성).
- 키 값은 `content/site.py`의 `INDEXNOW_KEY`.

## 2. Google — sitemap + Search Console (IndexNow 미참여)

구글은 IndexNow를 받지 않는다. 가장 빠른 정식 경로:

1. **Search Console**에 속성 등록 → `sitemap.xml` 제출 (1회)
2. 새 글은 Search Console **URL 검사 → 색인 생성 요청** (수동, 가장 확실)
3. (선택) `tools/google_indexing.py` — Indexing API. **공식적으론 JobPosting/
   BroadcastEvent 전용**이라 일반 페이지는 무시될 수 있음. 위 README 주석 참고.

## 3. 네이버 — 서치어드바이저

1. 메인 `<head>`의 `naver-site-verification` 으로 사이트 소유확인
2. 서치어드바이저에 `sitemap.xml`·`rss.xml` 제출
3. IndexNow(위 1번)로 즉시 통보까지 병행하면 가장 빠르다

> 참고: 구글·빙의 옛 `ping?sitemap=` 엔드포인트는 2023년 폐지되어 사용하지 않는다.
> 즉시 통보는 빙·네이버=IndexNow, 구글=Search Console/Indexing API 로 일원화한다.

## 배포 자동화(선택)

CI/CD에서 배포 직후 `python tools/indexnow.py` 한 줄을 추가하면 매 배포마다
변경 URL이 자동 통보된다.
