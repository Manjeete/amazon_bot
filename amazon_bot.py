from selenium import webdriver
from selenium.webdriver.firefox.options import Options


import re 
import time

class AmazonBot(object):
    def __init__(self, items):
        self.amazon_url = "https://www.amazon.ca/"
        self.items = items

        self.profile = webdriver.FirefoxProfile()
        self.options = Options
        self.driver = webdriver.Firefox() #"./geckodriver.exe", firefox_profile = self.profile, firefox_options=self.options
        self.driver.get(self.amazon_url)


    def search_items(self):
        urls = []
        names = []
        prices = []
        for item in self.items:
            print(f"Searching for {item}")
            self.driver.get(self.amazon_url)

            search_input = self.driver.find_element_by_id("twotabsearchtextbox")
            search_input.send_keys(item)
            time.sleep(2)

            search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
            search_button.click()
            time.sleep(2)

            first_result = self.driver.find_element_by_xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[2]')
            asin = first_result.get_attribute('data-asin')
            url = 'https://www.amazon.ca/dp/' + asin
            price = self.get_product_price(url)
            name = self.get_product_name(url)

            urls.append(url)
            prices.append(price)
            names.append(name)

            print(name)
            print(price)
            print(url)    
            time.sleep(2)

        return urls, prices, names

    def get_product_price(self, url):
        self.driver.get(url)
        try:
            price = self.driver.find_element_by_id("priceblock_ourprice").text
        except:
            pass

        try:
            price = self.driver.find_element_by_id("priceblock_dealprice").text
        except:
            pass

        if price is None:
            price = "Not Available"
        else:
            non_decimal = re.compile(r'[^\d.]+')
            price = non_decimal.sub('', price)    

        return price                    

    def get_product_name(self, url):
        self.driver.get(url)
        try:
            product_name = self.driver.find_element_by_id("productTitle").text
        except:
            pass

        if product_name is None:
            product_name = " Not Available"

        return product_name        


                