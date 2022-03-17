import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date


def get_data(product_type, product_url):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    driver.get(product_url)

    products_names = []
    products_link = []
    products_price = []
    products_old_price = []
    products_date = []
    products_type = []
    '''
        When the content page is dynamic, we need to anable a way to load
        the hiden html site content. In order to achieve that we are going 
        to use Selenium Lib
        to load dynamic elements.
        '''
    # Setting up a waiting time before scroll down
    SCROLL_PAUSE_TIME = 2.0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = BeautifulSoup(res, 'html.parser')

    # Get all the products name

    for contentName in soup.findAll(attrs={'class': 'containerDescripItemCarrusel__productName'}):
        products_names.append(contentName.text)
        products_date.append(date.today())
        products_type.append(product_type)

    # Get all the products link
    for contentLink in soup.findAll(attrs={'class': 'itemCarrusel__containerImgCarrusel containerImgItemCarrusel'}):
        # Get the Product Link
        for links in contentLink.find_all('a'):
            products_link.append(links.get('href'))

    # Get all the products price
    for contentPrice in soup.findAll(attrs={'class': 'containerPriceItemCarrusel__rowPrice'}):
        # Get the Product Name
        # Check if product is still available
        if contentPrice.find(class_="containerPriceItemCarrusel__priceNow"):
            products_price.append(contentPrice.find(class_="containerPriceItemCarrusel__priceNow").text)
            if contentPrice.find(class_="containerPriceItemCarrusel__priceOld"):
                products_old_price.append(contentPrice.find(class_="containerPriceItemCarrusel__priceOld").text)
            else:
                products_old_price.append("SIN OFERTA")
        else:
            products_price.append("AGOTADO")
            products_old_price.append("AGOTADO")

    product_table = pd.DataFrame(
        {'Tipo': products_type, 'Nombre': products_names, 'Links': products_link, 'Anterior': products_old_price,
         'Precios': products_price, 'Fecha': products_date})

    return product_table