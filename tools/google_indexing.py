#!/usr/bin/env python3
"""Google Indexing API — URL 색인 갱신 통보 (선택).

⚠️ 공식 주의: Google Indexing API 는 공식적으로 JobPosting · BroadcastEvent
구조화 데이터가 있는 페이지만 대상으로 합니다. 일반 페이지에도 호출은
되지만 구글이 무시할 수 있으며, 일반 페이지의 정식 경로는
sitemap.xml + Search Console 색인 요청입니다. 구글은 IndexNow 미참여.

사전 준비:
  1) Google Cloud 프로젝트에서 Indexing API 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드
  3) Search Console 속성에 그 서비스 계정 이메일을 '소유자'로 추가
  4) pip install google-auth requests

사용법:
  GOOGLE_APPLICATION_CREDENTIALS=service.json \
      python tools/google_indexing.py                # sitemap 전체
  GOOGLE_APPLICATION_CREDENTIALS=service.json \
      python tools/google_indexing.py <url> ...      # 지정 URL
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python build.py` 를 실행하세요.")
    return re.findall(r"<loc>([^<]+)</loc>", open(path, encoding="utf-8").read())


def main():
    cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred or not os.path.exists(cred):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 환경변수에 서비스 계정 JSON 경로를 지정하세요.")
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("pip install google-auth requests 후 다시 실행하세요.")

    creds = service_account.Credentials.from_service_account_file(cred, scopes=SCOPES)
    session = AuthorizedSession(creds)

    urls = [a for a in sys.argv[1:] if a.strip()] or sitemap_urls()
    print(f"Google Indexing API 통보 — {len(urls)} URL")
    for u in urls:
        r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"}, timeout=20)
        print(f"  [{r.status_code}] {u}")
    print("완료. (일반 페이지는 구글이 무시할 수 있으니 Search Console 색인요청을 함께 권장)")


if __name__ == "__main__":
    main()
