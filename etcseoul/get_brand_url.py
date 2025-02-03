import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # 상대 URL을 절대 URL로 변환하기 위해 사용
import pickle
import os

# from vars import *


def main():
    # 1. 대상 페이지 URL 및 요청 헤더 설정
    base_url = "https://www.etcseoul.com"  # 기본 도메인
    url = base_url + "/brand.html"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/95.0.4638.69 Safari/537.36")
    }
    
    # 2. 페이지 요청 및 HTML 가져오기
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
    except Exception as e:
        print("페이지 요청 중 오류 발생:", e)
        return

    # 3. BeautifulSoup을 사용해 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 4. 모든 .item_box 요소 찾기
    item_boxes = soup.select(".item_box")
    
    # 결과를 저장할 dictionary 선언
    brand_dict = {}
    
    for box in item_boxes:
        try:
            # 각 box 내부의 .item 요소 찾기
            item = box.select_one(".item")
            if not item:
                print("아이템 요소를 찾지 못했습니다.")
                continue
            
            # <a> 태그에서 href 추출
            a_tag = item.find("a")
            if not a_tag:
                print("아이템 안의 <a> 태그를 찾지 못했습니다.")
                continue
            href = a_tag.get("href")
            # 상대 URL인 경우 base_url을 붙여 절대 URL로 변환
            href = urljoin(url, href)
            
            # item 내부의 모든 <p> 태그 리스트에서 두 번째 <p> 태그의 텍스트 추출 (index 1)
            p_tags = item.find_all("p")
            if len(p_tags) >= 2:
                brand_name = p_tags[1].get_text(strip=True)
                # 딕셔너리에 추가 (브랜드명: 링크)
                brand_dict[brand_name] = href
            else:
                print("두 번째 <p> 태그를 찾을 수 없습니다.")
        except Exception as e:
            print("아이템 추출 중 에러 발생:", e)
    
    # 5. 결과를 pickle 파일로 저장
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(current_dir, 'brand_urls.pickle')

    try:
        with open(pickle_file_path, 'wb') as f:
            pickle.dump(brand_dict, f)
        print("pickle 파일 저장 완료:", pickle_file_path)
    except Exception as e:
        print("pickle 파일 저장 중 오류 발생:", e)

if __name__ == '__main__':
    main()
