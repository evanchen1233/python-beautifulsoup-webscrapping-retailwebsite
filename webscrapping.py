from bs4 import BeautifulSoup
import pandas as pd
import requests

def car_scrapping(url):
    
    agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    page = requests.get(url, headers=agent)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    lists = soup.find_all('div', class_="card mb-4 w-100 border border-0 border-warning")

    car = []
    for list in lists:
        price = list.find('h5', class_="mb-3 text-center").text.replace('\n', '').replace('$', '')
        price = price.replace(u' \xa0', u'')
        vehicles = list.find_all('li', style="list-style-type:none!important;font-size:15px;line-height:25px;text-align: left;")
        for vehicle in vehicles:
            vehicle = str(vehicle).split(">")[-2][:-4].replace('\xa0', '').replace('kms ', '').replace('kms', u'').replace('Year', '').replace(' model','')
            car.append(vehicle)
        
        car.append(price)
    return car


url= "https://www.sydneycars.com.au/"
agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
page = requests.get(url, headers=agent)

soup = BeautifulSoup(page.content, 'html.parser')
page_text = soup.find_all('a', class_="page-link")
pages = int(str(page_text).split(",")[-2].split(">")[-2][:-3])

car = []
for page in range(1, pages + 1):
    url = f"https://www.sydneycars.com.au/page/{page}/"
    
    car = car+ car_scrapping(url)
    
car = [car[i: i+5] for i in range(0, len(car), 5)]

df = pd.DataFrame(car, columns=['Model', 'Make Year','Transmission Type','Travelled (km)','Price ($)'])
print(df.head(100))