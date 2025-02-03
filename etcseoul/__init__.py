import requests
from bs4 import BeautifulSoup
import pickle
import os
from utils import (
    get_brand_description, 
    get_name_and_urls,
)
def main():
    # 현재 파일의 디렉토리를 기준으로 pickle 파일 경로 생성
    
    
    # 요청 헤더 설정 (User-Agent 등을 설정하여 일반 브라우저 요청처럼 보이게 합니다)
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/95.0.4638.69 Safari/537.36")
    }
    
    for brand, url in brand_urls_dict.items():
        print(f"\n===== {brand} =====")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        except Exception as e:
            print(f"{brand} 페이지 요청 중 오류 발생: {e}")
            continue
        

        #get brand description
        description = get_brand_description(response,brand)

        get_name_and_urls(response)
        break




if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(current_dir, 'brand_urls.pickle')
    
    # pickle 파일에서 브랜드명(key)과 URL(value) 딕셔너리 로드
    with open(pickle_file_path, 'rb') as f:
        brand_urls_dict = pickle.load(f)
    main()