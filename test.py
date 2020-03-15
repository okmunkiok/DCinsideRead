from selenium import webdriver
from bs4 import BeautifulSoup
import time

start_time = time.time()
url = "https://gall.dcinside.com/board/view/?id=classic&no=344693"
driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
print(time.time() - start_time)
print("end")
print("asdf")