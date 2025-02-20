from selenium.webdriver.chrome.options import Options
import os 
chrome_options = Options()
chrome_options.add_argument("--headless")  # headless 모드 사용
chrome_options.add_argument("--window-size=1920,1080")  # 화면 크기 설정

base_url = 'https://www.musinsa.com'


# target_brand_list = ['bronson','gramicci','arcteryx','patagonia']
target_brand_list = ['espionage']
brand_urls_dict = {brand: f'{base_url}/brand/{brand}' for brand in target_brand_list}
headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/95.0.4638.69 Safari/537.36")
}
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir,'images')
if not os.path.exists(image_dir):
    os.mkdir(image_dir)

for target_brand in target_brand_list:
    brand_image_dir = os.path.join(image_dir,target_brand)
    if not os.path.exists(brand_image_dir):
        os.mkdir(brand_image_dir)