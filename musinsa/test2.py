import time
import json
import gzip
from seleniumwire import webdriver  # Selenium 대신 seleniumwire 사용
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 옵션 설정 (headless 모드 및 화면 크기 지정)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

# Selenium Wire를 이용하여 Chrome WebDriver 생성
driver = webdriver.Chrome(options=chrome_options)

# 대상 페이지 열기
driver.get("https://www.musinsa.com/products/732698")

# WebDriverWait 객체 생성 (최대 10초 대기)
wait = WebDriverWait(driver, 10)

# 버튼 클릭 전 기존 네트워크 요청 초기화
# driver.requests.clear()

# data-button-id가 "prd_detail_open"인 버튼 요소 찾기
button = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button.gtm-click-button[data-button-id='prd_detail_open']")
))

# 버튼이 화면에 보이도록 스크롤 처리 후 JavaScript로 강제 클릭
driver.execute_script("arguments[0].scrollIntoView(true);", button)
driver.execute_script("arguments[0].click();", button)

# API 호출이 완료될 시간을 잠시 대기 (필요에 따라 조정)
time.sleep(3)

# 캡처된 네트워크 요청들 확인
for request in driver.requests:
    if request.response:
        # 예시: URL에 "api"라는 단어가 포함된 요청만 출력 (필요에 따라 필터링)
        if "api" in request.url:
            print("API 호출 URL:", request.url)
            print("HTTP 메서드:", request.method)
            print("응답 상태 코드:", request.response.status_code)
            try:
                # 응답 본문(바이트)을 가져옴
                body = request.response.body

                # 응답 헤더에서 Content-Encoding 확인 (gzip 등)
                encoding = request.response.headers.get("Content-Encoding", "")
                if "gzip" in encoding:
                    # gzip 압축 해제
                    body = gzip.decompress(body)
                
                # UTF-8로 디코딩
                decoded_body = body.decode("utf-8")
                print("응답 본문:", decoded_body)
                
                try:
                    # JSON 형식으로 파싱 시도
                    data = json.loads(decoded_body)
                    print("파싱된 JSON:", json.dumps(data, indent=2, ensure_ascii=False))
                except json.JSONDecodeError:
                    print("응답 본문이 JSON 형식이 아닙니다.")
            except Exception as e:
                print("응답 본문 디코딩 오류:", e)
            print("-" * 80)

driver.quit()

