import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from vars import base_url

def crawl_target_images(response):
    """
    지정한 URL의 HTML에서 src 속성에 '/web/upload/NNEditor/'가 포함된 <img> 태그의 절대 URL을 리스트로 반환합니다.
    """
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 전체 <img> 태그 중 src에 특정 패턴이 포함된 태그만 필터링
    target_imgs = soup.find_all('img', src=lambda s: s and '/web/upload/NNEditor/' in s)
    
    image_urls = []

    for img in target_imgs:
        src = img.get('src')
        # 상대 URL을 절대 URL로 변환
        absolute_url = urljoin(base_url, src)
        image_urls.append(absolute_url)

    unique_image_urls = list(dict.fromkeys(image_urls)) #순서 유지하면서 중복 제거 set을 쓰면 순서가 날라감

    return unique_image_urls

def download_images(image_urls, download_folder='images'):
    """
    추출된 이미지 URL 리스트를 받아 지정된 폴더에 이미지를 다운로드합니다.
    """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    download_paths = []
    for idx, img_url in enumerate(image_urls, start=1):
        try:
            print(f"[{idx}/{len(image_urls)}] 이미지 다운로드 중: {img_url}")
            response = requests.get(img_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"이미지 다운로드 실패: {img_url} / 에러: {e}")
            continue
        
        # URL에서 파일명을 추출 (예: .../EC9E91EC8381EC84B811.jpg)
        filename = img_url.split("/")[-1]
        file_path = os.path.join(download_folder, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        # print(f"저장 완료: {file_path}")
        download_paths.append(file_path)
    return download_paths
    

if __name__ == "__main__":
    # 크롤링할 페이지 URL을 실제 값으로 변경하세요.
    page_url = "https://www.etcseoul.com/product/detail.html?product_no=38821&cate_no=686&display_group=1"
    
    # 지정 패턴에 해당하는 이미지 URL들을 추출합니다.
    image_urls = crawl_target_images(page_url)
    
    if image_urls:
        print(f"추출된 이미지 수: {len(image_urls)}")
        # 추출된 이미지들을 다운로드합니다.
        download_images(image_urls)
    else:
        print("추출된 이미지가 없습니다.")
