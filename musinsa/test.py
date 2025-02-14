from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # headless 모드 사용
chrome_options.add_argument("--window-size=1920,1080")  # 화면 크기 설정
#chrome_options.add_argument("--no-sandbox")  # Linux 환경 등에서 추가 옵션

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.musinsa.com/products/4622135")  # 대상 URL


try:
    wait = WebDriverWait(driver, 30)
    
    # 2. 버튼 클릭하기
    #버튼이 클릭 가능한 상태를 기다립니다.
    button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.gtm-click-button[data-button-id='prd_detail_open']")
    ))
    
    # 버튼이 화면에 보이도록 스크롤 처리
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    
    # JavaScript를 이용하여 강제 클릭 (다른 요소에 가려진 경우에도 클릭)
    driver.execute_script("arguments[0].click();", button)
    
    # 3. 컨텐츠 로드 대기: 클래스가 "text-xs font-normal text-black font-pretendard" 인 모든 요소
    containers = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".text-xs.font-normal.text-black.font-pretendard")
    ))
    
    container = containers[-1]
    text_content = container.text
    if text_content:
        print("Text:", text_content)
    else :
        print('Text 형태로 저장되어있지 않습니다')

    # (c) <img> 태그의 src에서 .jpg 또는 .svg 파일 URL 추출
    imgs = container.find_elements(By.TAG_NAME, "img")
    image_urls = []
    for img in imgs:
        src = img.get_attribute("src")
        if src and ('.jpg' in src.lower() or '.svg' in src.lower()):
            image_urls.append(src)
     

finally:
    # 작업 완료 후 브라우저 종료
    driver.quit()
print(image_urls)