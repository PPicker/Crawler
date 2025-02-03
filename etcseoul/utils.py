from bs4 import BeautifulSoup


def get_brand_description(response):
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # <map name="categoryhead_top_image_map_name"> 요소를 찾습니다.
    map_element = soup.find('map', {'name': 'categoryhead_top_image_map_name'})
    if map_element:
        # 요소 내의 텍스트를 추출합니다.
        description = map_element.get_text(separator="\n").strip()
        return description
    else:
        return None