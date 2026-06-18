#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — Bing · Naver · Yandex · Seznam 공용.

IndexNow 프로토콜은 참여 검색엔진(빙·네이버·얀덱스 등)에 URL 변경을
즉시 알려 색인을 앞당긴다. 구글은 IndexNow에 참여하지 않으므로
구글은 sitemap.xml + Search Console(또는 tools/google_indexing.py)을 사용한다.

사용법:
  python tools/indexnow.py                # sitemap.xml 의 모든 URL 일괄 통보
  python tools/indexnow.py <url> [<url>]  # 지정한 URL만 통보 (글 올릴 때마다)

키 파일: 빌드 시 사이트 루트에 {INDEXNOW_KEY}.txt 가 생성되어
        https://<도메인>/{KEY}.txt 로 검증된다.
의존성 없음(파이썬 표준 라이브러리만 사용).
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
HOST = re.sub(r"^https?://", "", BASE).split("/")[0]
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"

# 참여 엔진 엔드포인트 — 하나만 보내도 공유되지만, 속도를 위해 모두 통보.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
    "https://yandex.com/indexnow",
]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python build.py` 를 실행하세요.")
    txt = open(path, encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", txt)


def submit(urls):
    payload = json.dumps({
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")

    for ep in ENDPOINTS:
        req = urllib.request.Request(
            ep, data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                print(f"  [{resp.status}] {ep}")
        except urllib.error.HTTPError as e:
            # 200/202 외에도 일부 엔진은 비표준 코드를 반환한다.
            print(f"  [{e.code}] {ep}  ({e.reason})")
        except Exception as e:  # noqa: BLE001
            print(f"  [ERR] {ep}  {e}")


def main():
    args = [a for a in sys.argv[1:] if a.strip()]
    urls = args if args else sitemap_urls()
    if not urls:
        sys.exit("통보할 URL 이 없습니다.")
    # 모든 URL 은 등록된 host 와 같은 도메인이어야 한다.
    bad = [u for u in urls if not u.startswith(BASE)]
    if bad:
        sys.exit(f"다른 도메인 URL 은 통보할 수 없습니다: {bad[:3]}")
    print(f"IndexNow 통보 — host={HOST}, {len(urls)} URL")
    submit(urls)
    print("완료. 빙·네이버·얀덱스에 통보했습니다. (구글은 sitemap/Search Console 사용)")


if __name__ == "__main__":
    main()
