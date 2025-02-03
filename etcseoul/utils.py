from bs4 import BeautifulSoup
from urllib.parse import urljoin
from vars import base_url,headers
import requests
import re


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
    


def get_name_and_urls(response):
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
                print("check\n")
                print(price_text)
                print("check\n")
                if "원" in price_text:
                    print("가격 정보 있음:", price_text)
                    response = requests.get(product_href, headers=headers)
                    get_info(response)
                    # exit()
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
        for div in detail_divs:
            print(div.get_text(separator="\n", strip=True))
    else:
        print("PC용 detail 영역을 찾지 못했습니다.")
