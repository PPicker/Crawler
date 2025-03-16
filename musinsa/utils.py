import vars
from bs4 import BeautifulSoup
import json 
import requests
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



def get_brand_description(response,brand):
    html = response.text
    # 받아온 HTML을 BeautifulSoup으로 파싱
    soup = BeautifulSoup(html, 'html.parser')
    
    # 예시: __NEXT_DATA__라는 id를 가진 스크립트 태그에서 JSON 데이터 추출
    next_data_script = soup.find("script", id="__NEXT_DATA__")
    # if next_data_script:
    #     json_text = next_data_script.string.strip()
    #     data = json.loads(json_text)
    #     # 페이지의 메타데이터 부분 추출 (예: props -> pageProps -> meta)
    #     brand_meta = data.get("props", {}).get("pageProps", {}).get("meta", {})
    #     print("브랜드 메타데이터:")
    #     print(brand_meta)
    # else:
    #     print("필요한 스크립트 태그를 찾지 못했습니다.")

    json_text = next_data_script.string.strip()
    data = json.loads(json_text)
    # 페이지의 메타데이터 부분 추출 (예: props -> pageProps -> meta)
    brand_meta = data.get("props", {}).get("pageProps", {}).get("meta", {})
    # print("브랜드 메타데이터:")
    # print(brand_meta)
    brand_name = brand_meta['brandName']
    brand_eng_name = brand_meta['brandNameEng']
    description = brand_meta['introduction']
    return f'{brand_name}({brand_eng_name})', description



# https://api.musinsa.com/api2/dp/v1/plp/goods?brand=arcteryx&gf=M&sortCode=POPULAR&category=002&page=1&size=30&caller=BRAND
# Request Method:
# GET


def get_brand_products(response,brand):
    brand_image_dir = os.path.join(vars.image_dir,brand)
    #brand_image_dir = os.path.join("images", "espionage") #상대 경로로 쓰기
    products_data = []
    product_base_url = "https://api.musinsa.com/api2/dp/v1/plp/goods"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    params = {
        "brand": f"{brand}",  # 원하는 브랜드
        "sortCode": "POPULAR",
        "page": 1,           # 시작 페이지 번호
        "size": 30,          # 한 페이지당 제품 수
        "caller": "FLAGSHIP",
        'gf' : "M", #성별 남자 , 여성은 F, 전체는 A임
        'category' : '001' #001 : 상의, 002 : 아우터, 003 : 하의
    }

    category_dicts = {'001':'TOP', '002' : 'OUTER', '003' : 'BOTTOM' }
    all_products = []
    for key, value in category_dicts.items():
        params["page"] = 1 #초기화해줌
        params['category'] = key
        print(f'{key} 카테고리를 추출합니다')
        while True:
            # API 요청 보내기
            response = requests.get(product_base_url, params=params, headers=headers)
            
            # 응답을 JSON으로 파싱
            json_data = response.json()
            
            # 제품 데이터는 data.list 에 있음
            products = json_data.get("data", {}).get("list", [])
            products = [{**product, 'category': value} for product in products] #category 추가
            
            all_products.extend(products[:5]) #일단 10개로 고정
            #print(len(products))
            # 페이지 정보 확인 (pagination 안에 hasNext가 있음)
            pagination = json_data.get("data", {}).get("pagination", {})
            has_next = pagination.get("hasNext", False)
            has_next = False #일단 페이지 넘기지 마
            print(f"페이지 {params['page']}에서 {len(products)}개의 제품 수집")
            
            # 다음 페이지가 없으면 종료
            if not has_next:
                print("더 이상 페이지가 없습니다. 종료합니다.")
                break
            params["page"] += 1
    #print(f"총 수집된 제품 개수: {len(all_products)}")
    descriptions =get_description_from_url(all_products)
    # exit()
    for product,description in zip(all_products,descriptions):
        #print(product['goodsName'])
        
        product_name = product['goodsName'].replace(' ','_') #공백은 _로 변환
        # print(product_name)
        # exit()
        link = product['goodsLinkUrl']
        thumbnail_image = product['thumbnail']
        price = product['price']
        image_path = brand + '_' + product_name + '.' + thumbnail_image.split('.')[-1]
        image_path = os.path.join(brand_image_dir,image_path)
        download_image(thumbnail_image,image_path)
        # relative_image_path = os.path.relpath(image_path, start=os.getcwd())
        products_data.append([product_name,brand,link,price,description,os.path.relpath(image_path, start=os.path.dirname(os.path.abspath(__file__)))])

    return products_data

def get_description_from_url(products):
    descriptions = []
    # WebDriver 초기화 (한 번만 생성)
    driver = webdriver.Chrome(options=vars.chrome_options)
    try:
        for product in products:
            try:
                # print(product)
                # print(product['goodsName'])
                product_name = product['goodsName']
                link = product['goodsLinkUrl']
                thumbnail_image = product['thumbnail']
                
                # 대상 URL 이동 (예시 URL, 실제 URL로 변경 필요)
                driver.get(link)

                wait = WebDriverWait(driver, 30)
                
                # 2. 버튼 클릭하기: 버튼이 클릭 가능한 상태를 기다립니다.
                button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.gtm-click-button[data-button-id='prd_detail_open']")
                ))
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                driver.execute_script("arguments[0].click();", button)
                
                # 3. 컨텐츠 로드 대기: 클래스가 "text-xs font-normal text-black font-pretendard"인 모든 요소
                containers = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".text-xs.font-normal.text-black.font-pretendard")
                ))
                
                # 필요한 경우, 마지막 요소 대신 모든 요소를 순회할 수도 있음
                container = containers[-1]
                text_content = container.text
                if text_content:
                    descriptions.append(text_content)
                else:
                    '''
                    text가 없는 경우에만 image를 뽑도록 로직 조정
                    '''
                    print('Text 형태로 저장되어있지 않습니다')
                    descriptions.append('') #일단 공백 보내
                    # # (c) <img> 태그의 src에서 .jpg 또는 .svg 파일 URL 추출
                    # imgs = container.find_elements(By.TAG_NAME, "img")
                    # image_urls = []
                    # for img in imgs:
                    #     src = img.get_attribute("src")
                    #     if src and ('.jpg' in src.lower() or '.svg' in src.lower()):
                    #         image_urls.append(src)
                    
                    # print("Image URLs:", image_urls)
            
            except Exception as e:
                # 각 상품 처리 시 예외 발생해도 다음 상품 처리를 계속할 수 있음
                print(f"Error processing product {product['goodsName']}: {e}")
    finally:
        # 모든 상품 처리 후에 드라이버 종료
        driver.quit()
    return descriptions





def download_image(image_url, filename):
    """
    주어진 URL의 이미지를 다운로드하여 지정한 파일명으로 저장합니다.

    Parameters:
        image_url (str): 다운로드할 이미지의 URL.
        filename (str): 저장할 파일명 (경로 포함 가능).
    """
    try:
        # 이미지 다운로드 요청
        response = requests.get(image_url)
        response.raise_for_status()  # 요청이 실패할 경우 예외 발생

        # 바이너리 모드로 파일 저장
        with open(filename, "wb") as file:
            file.write(response.content)
        #print(f"이미지가 '{filename}'로 성공적으로 저장되었습니다.")
        
    except requests.exceptions.RequestException as e:
        print(f"이미지 다운로드에 실패했습니다: {e}")