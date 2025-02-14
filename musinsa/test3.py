import requests
from bs4 import BeautifulSoup

# 대상 URL (필요에 따라 변경)
url = "https://www.musinsa.com/products/4622135"

# HTTP 헤더 (User-Agent 등 지정하면 서버에서 정상 응답을 받을 확률이 높아집니다)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}

# 웹 페이지 요청
response = requests.get(url, headers=headers)
html_content = response.text

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# CSS 선택자를 사용하여 클래스가 "text-xs font-normal text-black font-pretendard" 인 요소 선택
elements = soup.select(".text-xs.font-normal.text-black.font-pretendard")

# 선택된 요소의 텍스트 출력
for el in elements:
    print(el.get_text(strip=True))
