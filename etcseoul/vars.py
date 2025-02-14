'''
global variable을 여기에서 저장 및 관리
'''



import os 
import pickle

# target_brands = ['']


headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/95.0.4638.69 Safari/537.36")
}

base_url =  "https://www.etcseoul.com"

current_dir = os.path.dirname(os.path.abspath(__file__))
pickle_file_path = os.path.join(current_dir, 'brand_urls.pickle')

# pickle 파일에서 브랜드명(key)과 URL(value) 딕셔너리 로드
with open(pickle_file_path, 'rb') as f:
        brand_urls_dict = pickle.load(f)


