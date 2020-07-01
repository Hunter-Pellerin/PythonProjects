from selenium import webdriver
from time import sleep

class AmazonScraper:
    _browser = None
    _products = []

    def __init__(self):
        self._browser = webdriver.Chrome("/usr/bin/chromedriver")
        self._browser.get("https://amazon.com")
        sleep(2)

    def searchForProduct(self, productName):
        searchBox = self._browser.find_element_by_xpath("//*[@id=\"twotabsearchtextbox\"]")
        searchBox.send_keys(productName)
        searchButton = self._browser.find_element_by_xpath("//input[@type=\"submit\"]")
        searchButton.click()

    def getProducts(self):
        productElements = self._browser.find_elements_by_xpath("//span[@class=\"a-size-medium a-color-base a-text-normal\"]")
        for product in productElements:
            self._products.append(product.text)
        return self._products

    def _getProductRows(self):
        rows = self._browser.find_elements_by_class_name("sg-row")
        return rows

    def getPrices(self):
        prices = []
        cent = []
        dollars = self._browser.find_elements_by_class_name("a-price-whole")
        cents = self._browser.find_elements_by_class_name("a-price-fraction")

        for price in dollars:
            prices.append(price.text)
        for price in cents:
            cent.append(price.text)
        for x in range(0, len(prices)):
            prices.insert(x, prices[x] + '.' + cent[x])
            prices.pop(x+1)
        return prices

    def quit(self):
        self._browser.quit()

scraper = AmazonScraper()
scraper.searchForProduct("24-inch QHD Monitor")
print(scraper.getProducts())
print(scraper.getPrices())
