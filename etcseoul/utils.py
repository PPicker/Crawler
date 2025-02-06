from bs4 import BeautifulSoup
from urllib.parse import urljoin
from vars import base_url,headers
import requests
import re
from get_image import crawl_target_images,download_images




def get_brand_description(response,brand):
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # <map name="categoryhead_top_image_map_name"> 요소를 찾습니다.
    map_element = soup.find('map', {'name': 'categoryhead_top_image_map_name'})
    if map_element:
        # 요소 내의 텍스트를 추출합니다.
        description = map_element.get_text(separator="\n").strip()
        return description
    else:
        print(f"{brand} 페이지에서 브랜드 설명 요소를 찾지 못했습니다.")
        return None




def get_item_data(response,brand=None):
    '''
    brand 페이지 html을 입력으로 받아서 제품명, 브랜드, 가격, 제품 Url, 제품 설명, 제품 이미지 주소 리스트를 반환함
            
    '''
    price_pattern = r"\s*:\s*(\d{1,3}(?:,\d{3})*원)(?:\s*:\s*(\d{1,3}(?:,\d{3})*원))?"
    html = response.text
    # BeautifulSoup 객체 생성 (파서로는 'html.parser'를 사용)
    soup = BeautifulSoup(html, 'html.parser')

    # 모든 상품 li 태그를 찾습니다.
    # li 태그의 class가 "item xans-record-" 인 요소들을 모두 선택합니다.
    # li 태그 중 클래스명이 "item xans-record-" 인 요소를 모두 선택합니다.
    product_info_list = []
    for item in soup.select('li.item.xans-record-'):
        # a 태그 중 클래스명이 "name"인 요소 선택 (앞뒤 공백 없이)
        a_tag = item.select_one('a.name')
        if a_tag: #item이 있는 경우
            product_name = None
            product_href = None
            product_price = None
            product_detail = None
            product_image_paths = None
            # 상품명 추출 (내부의 모든 텍스트를 공백 제거하여 가져옴)
            product_name = a_tag.get_text(strip=True) #상품명
            # href 속성 값 추출 (상대 URL일 경우 절대 URL로 변환)
            product_href = urljoin(base_url, a_tag.get('href')) #상품 페이지
        

            price_info_block = item.select_one("ul.xans-product-listitem")
            if price_info_block:
                # 블록 내부 텍스트를 추출 (여러 li 태그가 공백 구분으로 합쳐짐)
                price_text = price_info_block.get_text(" ", strip=True)
                # 가격 단위 "원"이 포함되어 있는지 확인

                if "원" in price_text:
                    print("가격 정보 있음:", price_text)
                    match = re.search(price_pattern, price_text)
                    # 그룹 2(할인가)가 있으면 그걸 사용하고, 없으면 그룹 1(원래 가격)을 사용.
                    product_price = match.group(2) if match.group(2) else match.group(1) #가격

                    response = requests.get(product_href, headers=headers) #상품 페이지로 진입
                    product_detail = get_info(response) #상품 detail 뽑음

                    image_urls = crawl_target_images(response)
                    if image_urls:
                        print(f"추출된 이미지 수: {len(image_urls)}")
                        # 추출된 이미지들을 다운로드합니다.
                        product_image_paths = download_images(image_urls) #image 적재 경로
                    else:
                        print("추출된 이미지가 없습니다.")
                    
                    product_info_list.append([product_name,brand,product_href,product_price,product_detail,product_image_paths])
                else:
                    print("가격 정보 없음.") #가격정보 없는 경우는 추가하지말고 걍 넘겨버리자
        #product_info_list.append([product_name,brand,product_href,product_price,product_detail,product_image_paths])
    return product_info_list



def get_name_and_urls(response):
    price_pattern = r"\s*:\s*(\d{1,3}(?:,\d{3})*원)(?:\s*:\s*(\d{1,3}(?:,\d{3})*원))?"
    html = response.text
    # BeautifulSoup 객체 생성 (파서로는 'html.parser'를 사용)
    soup = BeautifulSoup(html, 'html.parser')

    # 모든 상품 li 태그를 찾습니다.
    # li 태그의 class가 "item xans-record-" 인 요소들을 모두 선택합니다.
    # li 태그 중 클래스명이 "item xans-record-" 인 요소를 모두 선택합니다.
    for item in soup.select('li.item.xans-record-'):
        # a 태그 중 클래스명이 "name"인 요소 선택 (앞뒤 공백 없이)
        a_tag = item.select_one('a.name')
        if a_tag:
            # 상품명 추출 (내부의 모든 텍스트를 공백 제거하여 가져옴)
            product_name = a_tag.get_text(strip=True)
            # href 속성 값 추출 (상대 URL일 경우 절대 URL로 변환)
            product_href = urljoin(base_url, a_tag.get('href'))
            

            print("상품명:", product_name)
            print("링크:", product_href)

            price_info_block = item.select_one("ul.xans-product-listitem")
            if price_info_block:
                # 블록 내부 텍스트를 추출 (여러 li 태그가 공백 구분으로 합쳐짐)
                price_text = price_info_block.get_text(" ", strip=True)
                # 가격 단위 "원"이 포함되어 있는지 확인

                if "원" in price_text:
                    print("가격 정보 있음:", price_text)
                    match = re.search(price_pattern, price_text)
                    # 그룹 2(할인가)가 있으면 그걸 사용하고, 없으면 그룹 1(원래 가격)을 사용.
                    price = match.group(2) if match.group(2) else match.group(1)
                    print(f'최종가격 : {price}')

                    response = requests.get(product_href, headers=headers)
                    detail = get_info(response)

                    image_urls = crawl_target_images(response)
                    if image_urls:
                        print(f"추출된 이미지 수: {len(image_urls)}")
                        # 추출된 이미지들을 다운로드합니다.
                        download_images(image_urls)
                    else:
                        print("추출된 이미지가 없습니다.")

                else:
                    print("가격 정보 없음.")



            

def get_info(response):
    html = response.text
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html, 'html.parser')
    detail_wrap_div = soup.find("div", class_="xans-element- xans-product xans-product-detail detail_wrap")
    if detail_wrap_div:
        # detail_wrap_div 내부에서 style="text-align: center;" 속성을 가진 모든 <div>를 찾음
        detail_divs = detail_wrap_div.find_all("div", style="text-align: center;")
        # for div in detail_divs:
        #     print(div.get_text(separator="\n", strip=True))
        #     return 
        return [div.get_text(separator="\n", strip=True) for div in detail_divs]
    else:
        print("PC용 detail 영역을 찾지 못했습니다.")
        return None 
