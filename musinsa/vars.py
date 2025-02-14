

base_url = 'https://www.musinsa.com'


target_brand_list = ['bronson','gramicci','arcteryx','patagonia']

brand_urls_dict = {brand: f'{base_url}/brand/{brand}' for brand in target_brand_list}

# brand_urls_dict = ['']


headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/95.0.4638.69 Safari/537.36")
}

# print((brand_urls_dict))
