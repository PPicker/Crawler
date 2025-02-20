from typing import List 
import os
from vars import (
    brand_urls_dict,
    headers
)

from utils import (
    get_brand_description,
    get_brand_products,
)

import requests
import csv


def crawling(brands: List[str] = None) -> None:
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    brand_csv_path = os.path.join(current_dir, 'brands.csv')
    item_csv_path = os.path.join(current_dir, 'items.csv')

    if brands is None:  # 브랜드 리스트가 지정되지 않으면 전체 브랜드 가져오기
        brands = list(brand_urls_dict.keys())

    brand_data_list = []  # 브랜드 데이터를 저장할 리스트
    item_data_list = []

    for brand in brands:
        print(brand)
        url = brand_urls_dict[brand]
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        except Exception as e:
            print(f"{brand} 페이지 요청 중 오류 발생: {e}")
            continue

        #brand description부터 추출
        name, description = get_brand_description(response, brand) 
        brand_data_list.append([name,url,description]) #list에 추가
        # item_data_list += get_item_data(response,brand)

        item_data_list=get_brand_products(response,brand)


    # # # CSV 파일에 데이터 저장 
    # # '''
    # # 왜 한번에 저장하고 쓰는 방식을 선택? 
    # # 브랜드가 지나치게 많으면 리스트에 한번에 담는게 메모리 부하가 클 수 있음
    # # 그런데 지금은 그정도로 많지 않음 그러니 IO bound를 낮추는게 더 효과적이라 판단
    # # '''

    with open(item_csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Brand", "Link","Price","Description",'Image_paths'])  # 헤더 작성
        writer.writerows(item_data_list)  # 데이터 작성

    with open(brand_csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Brand", "URL", "Description"])  # 헤더 작성
        writer.writerows(brand_data_list)  # 데이터 작성






if __name__ == '__main__':
    target_brand_list = None #specify 하고싶은 경우 그렇게 진행
    crawling(target_brand_list)