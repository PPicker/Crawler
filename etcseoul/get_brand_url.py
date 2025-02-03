
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os

if __name__ == '__main__':

    # 1. 옵션 설정 (원하는 경우 Headless 모드 사용)
    options = Options()
    # options.headless = True  # headless 모드를 원하면 주석을 해제하세요.

    # 2. 웹 드라이버 실행 (Chrome 예제)
    driver = webdriver.Chrome(options=options)

    try:
        # 3. 대상 페이지 열기 (실제 URL로 수정)
        driver.get("https://www.etcseoul.com/brand.html")
        
        # 4. 페이지 로딩이 완료될 때까지 대기 (예: .item_box 요소가 로드될 때까지)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".item_box")))
        
        # 5. 모든 item_box 요소 찾기
        item_boxes = driver.find_elements(By.CSS_SELECTOR, ".item_box")
        
        # 결과를 저장할 dictionary 선언
        brand_dict = {}
        
        for box in item_boxes:
            try:
                # 각 box 내부의 item 요소 찾기
                item = box.find_element(By.CSS_SELECTOR, ".item")
                
                # <a> 태그에서 href 추출
                a_tag = item.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute("href")
                
                # 두 번째 <p> 태그에서 브랜드명 추출
                # item 내부의 모든 <p> 요소 리스트를 가져온 후 두 번째 요소 사용 (index 1)
                p_tags = item.find_elements(By.TAG_NAME, "p")
                if len(p_tags) >= 2:
                    brand_name = p_tags[1].text.strip()
                    # 딕셔너리에 추가 (브랜드명: 링크)
                    brand_dict[brand_name] = href
                # else:
                #     print("두 번째 <p> 태그를 찾을 수 없습니다.")
            except Exception as e:
                print("아이템 추출 중 에러 발생:", e)
        #결과 출력

    finally:
        # 6. 작업 완료 후 드라이버 종료
        driver.quit()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    #폴더 내에 brand_urls.pickle 파일 경로 생성
    pickle_file_path = os.path.join(current_dir, 'brand_urls.pickle')
    with open(pickle_file_path,'wb') as f:
        pickle.dump(brand_dict,f)
