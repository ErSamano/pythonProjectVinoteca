import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date


def get_data(product_type, product_url):

    driver = webdriver.Firefox()  # Use Firefox, Chrome, etc. depending on your preference
    driver.set_window_size(2304, 1440)
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
    SCROLL_PAUSE_TIME = 4.0

    # Click "Soy Mayor de 18 años" button
    try:
        age_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//button[contains(@class, "vicomstudio-modal-layout-0-x-closeButton") and .//span[text()="Soy Mayor de 18 Años"]]'))
        )
        age_button.click()
    except Exception as e:
        print("Could not find or click Vinoteca Age button.")

    # Click "Aceptar cookies" button
    try:
        # Wait for the button to be present in the DOM
        driver.execute_script("document.getElementById('zendesk-fake-btn').style.display = 'none';")
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                # (By.XPATH,
                #  '//button[contains(@class, "vicomstudio-modal-layout-0-x-closeButton")]//span[text()="Aceptar"]')
                (By.XPATH,
                 '//span[contains(@class, "vicomstudio-modal-layout-0-x-closeButtonLabel") and contains(@class, "vicomstudio-modal-layout-0-x-closeButtonLabel--CookiesAdversimentClose")]')

            )
        )

        # # Then wait for the button to be clickable
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        #
        # # Then click the button
        # button.click()
        driver.execute_script("arguments[0].click();", button)

    except Exception as e:
        print("Could not find or click Vinoteca Aceptar cookies button.", e)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        time.sleep(SCROLL_PAUSE_TIME)
        # Scroll down to 3/4 of the page height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.80);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    while True:
        # Locate the 'Mostrar más' button
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class, "vtex-button") and .//div[text()="Mostrar más"]]'))
            )
            show_more_button.click()
            time.sleep(SCROLL_PAUSE_TIME)
        except Exception as e:
            # The button is not available or not clickable anymore
            break

    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = BeautifulSoup(res, 'html.parser')
    # Get all the products name

    for contentName in soup.findAll(attrs={'class': 'vtex-product-summary-2-x-brandName'}):
        products_names.append(contentName.text)
        products_date.append(date.today())
        products_type.append(product_type)

    # Get all the products link
    for contentLink in soup.findAll(attrs={'class': 'vtex-product-summary-2-x-containerNormal'}):
        # Get the Product Link
        for links in contentLink.find_all('a'):
            products_link.append("https://www.vinoteca.com"+links.get('href'))

    def extract_price(price_tag):
        currency_code = price_tag.find(class_='vtex-product-price-1-x-currencyCode').text
        currency_parts = []
        for part in price_tag.find_all(['span']):
            if 'vtex-product-price-1-x-currencyInteger' in part['class']:
                currency_parts.append(part.text)
            elif 'vtex-product-price-1-x-currencyGroup' in part['class']:
                continue
            elif 'vtex-product-price-1-x-currencyDecimal' in part['class']:
                break
        currency_integer = ''.join(currency_parts)
        currency_decimal = price_tag.find(class_='vtex-product-price-1-x-currencyDecimal').text
        currency_fraction = price_tag.find(class_='vtex-product-price-1-x-currencyFraction').text
        return f"{currency_code}{currency_integer}{currency_decimal}{currency_fraction}"

    # Get all the products price
    for contentPrice in soup.findAll(attrs={'class': 'vtex-flex-layout-0-x-flexRowContent--ProductItem-Price'}):

        selling_price_tag = contentPrice.find(class_='vtex-product-price-1-x-sellingPriceValue')
        if selling_price_tag:
            selling_price = extract_price(selling_price_tag)
            products_price.append(selling_price)
        else:
            products_price.append("AGOTADO")

        list_price_tag = contentPrice.find(class_='vtex-product-price-1-x-listPriceValue')
        if list_price_tag:
            list_price = extract_price(list_price_tag)
            products_old_price.append(list_price)
        else:
            products_old_price.append("SIN OFERTA")

    product_table = pd.DataFrame(
        {'Tipo': products_type, 'Nombre': products_names, 'Links': products_link, 'Anterior': products_old_price,
         'Precios': products_price, 'Fecha': products_date})

    return product_table