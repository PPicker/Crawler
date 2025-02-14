import requests
from bs4 import BeautifulSoup
from typing import List
import pickle
import os
import csv
from utils import (
    get_brand_description, 
    get_name_and_urls,
    get_item_data
)
from  vars import (
    brand_urls_dict,
    headers
)



# class Crawler():
#     def __init__(self,brands: List[str] = None):
#         if brands is None:  # 브랜드 리스트가 지정되지 않으면 전체 브랜드 가져오기
#             brands = list(brand_urls_dict.keys())
#         self.brands = brands
#         self.brand_urls_dict = brand_urls_dict
#         self.brand_data_list = []

#     def crawling_brand(self):

'''
class vs function
크롤러를 클래스로 짜냐 함수로 짜냐에 대한 고민
클래스로 짜는게 예쁘긴함 그런데 크롤링이라는 과정 자체가 서로 엮여있고 하나의 full sequence로 이루어진 느낌이라
서로 다른 function이 독립적이기보다 연쇄적임 이럴거면 걍 하나의 함수로 묶는게 좋아보임
brand를 크롤링한다했을 때 -> brand -> 하위 프로덕트 쭉
이렇게 묶이는데 뭐하러 굳이 따로 분리하나 싶음

'''



def crawling(brands: List[str] = None) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    brand_csv_path = os.path.join(current_dir, 'brands.csv')
    item_csv_path = os.path.join(current_dir, 'items.csv')

    if brands is None:  # 브랜드 리스트가 지정되지 않으면 전체 브랜드 가져오기
        brands = list(brand_urls_dict.keys())

    brand_data_list = []  # 브랜드 데이터를 저장할 리스트
    item_data_list = []

    for brand in brands:
        url = brand_urls_dict[brand]
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        except Exception as e:
            print(f"{brand} 페이지 요청 중 오류 발생: {e}")
            continue

        #brand description부터 추출
        description = get_brand_description(response, brand) 
        brand_data_list.append([brand,url,description]) #list에 추가
        item_data_list += get_item_data(response,brand)


    # # CSV 파일에 데이터 저장 
    # '''
    # 왜 한번에 저장하고 쓰는 방식을 선택? 
    # 브랜드가 지나치게 많으면 리스트에 한번에 담는게 메모리 부하가 클 수 있음
    # 그런데 지금은 그정도로 많지 않음 그러니 IO bound를 낮추는게 더 효과적이라 판단
    # '''

    with open(item_csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # product_info_list.append([product_name,brand,product_href,product_price,product_detail,product_image_paths])
        writer.writerow(["Name", "Brand", "Link","Price","Description",'Image_paths'])  # 헤더 작성
        writer.writerows(item_data_list)  # 데이터 작성

    with open(brand_csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Brand", "URL", "Description"])  # 헤더 작성
        writer.writerows(brand_data_list)  # 데이터 작성






if __name__ == '__main__':
    target_brand_list = ['Art if acts']
    #target_brand_list = None
    crawling(target_brand_list)