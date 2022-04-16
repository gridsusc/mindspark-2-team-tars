from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher
import requests

def get_similarity(string1, string2):
    '''
    Get similarity between two food names
    param: string1: string
    param: string2: string
    return: ratio: float
    '''
    ratio = SequenceMatcher(None, string1.lower(), string2.lower()).ratio()
    return ratio

def clean_name(name):
    '''
    Tidy up the food name
    param: name: string
    return: name: string
    '''
    return name.split("[")[0]

def check_if_present(food_name):
    '''
    Given a food name returns True if it is already present in our existing DB
    param: food_name: string
    return: Boolean
    '''
    cleaned_food_name = clean_name(food_name)
    food_items = pd.read_csv('final.csv')['Category']
    for food in food_items:
        ratio = get_similarity(food, cleaned_food_name)
        if ratio > 0.7:
            return True
    return False

def get_food_urls(url):
    '''
    Given a product url returns each products' href links
    param: url: string
    return: hrefs: list of strings 
    '''
    hrefs = []
    food_page = requests.get(url + '&page=1&per_page=50000')
    food_page_soup = BeautifulSoup(food_page.text, "lxml")

    food_divs = food_page_soup.find_all("div", {"id": "product_ind_result"})
    for div in food_divs:
        new_food_name = div.find('div', {'class': 'ind_result_text'}).find('a').get_text()
        if check_if_present(new_food_name) == False:
            hrefs.append("https://www.ewg.org" + div.find("a")['href'])
    return hrefs

def get_category_urls(id):
    '''
    Given a product id returns each category urls
    param: id: string
    return: category_url: list of strings 
    '''
    category_urls =[]
    food_page = requests.get("https://www.ewg.org/foodscores/products/#")
    food_page_soup = BeautifulSoup(food_page.text, "lxml")
    category_a = food_page_soup.find("ul", {"id": id}).find_all('a')
    for anchor in category_a:
        category_urls.append("https://www.ewg.org" + anchor['href'])
    return category_urls

total_hrefs = []
category_urls = get_category_urls("cannedgoodssoups_ul")
category_urls.append("https://www.ewg.org/foodscores/products/?category_group=Tofu+%26+Meat+Alternatives")
for url in category_urls:
    print(url)
    hrefs = get_food_urls(url)
    print(len(hrefs))
    total_hrefs += hrefs
print("TOTAL")
print(len(total_hrefs))

df = pd.DataFrame(total_hrefs, columns=["colummn"])
df.to_csv('urls.csv', index=False)