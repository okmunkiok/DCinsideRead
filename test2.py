import DCinsideRead.dcinside as dc
import DCinsideRead.common as common
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd

if __name__ == "__main__":
    page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("국내야구")
    url = "https://gall.dcinside.com/board/view/?id=classic&no=345728&t=cv"
    url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=8225358&exception_mode=recommend&page=215"
    url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=13967163&t=cv&exception_mode=recommend&page=1"
    # url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=830565&t=cv"
    # url = "https://gall.dcinside.com/board/view/?id=event_voicere&no=2225574&exception_mode=recommend&page=1"
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver_page_source_list = []
    # print(len(driver_page_source))
    # print(type(driver_page_source))
    # print(driver_page_source)
    dc.get_reply_all_html(driver_page_source_list=driver_page_source_list, driver=driver)
    # driver_page_source_merged = "".join(driver_page_source)
    # date_list = []
    reply_dictionary = {}
    for driver_page_source in driver_page_source_list:
        bs = BeautifulSoup(driver_page_source, "html.parser")
        regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
        contents = bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)})
        # print(type(contents))
        regular_expression_for_getting_reply = r"reply_li_[^0]\w*"
        contents.extend(bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)}))

        for content in contents:
            reply_dictionary[len(reply_dictionary)] = {
                "date": dc.get_reply_date(content),
                "title": dc.get_reply_title(content),
                "writer": dc.get_reply_writer(content),
                "ip": dc.get_reply_ip(content)
            }

    df = pd.DataFrame(reply_dictionary).transpose()

    csv_path_and_name = dc.get_csv_path_and_name(
        common.get_directories_dictionary("dcinside")["temp_raw_data_path"], page_and_base_url_dictionary,
        post_number_from=1, post_number_to=1 + 50, read_post_reply=True)
    df.to_csv(csv_path_and_name)

    reply_dictionary.clear()

            # date_list.append(dc.get_reply_date(content))
    # print(reply_dictionary)
    # print(len(reply_dictionary))
    # print(date_list)
    # print(len(date_list))
    # print(driver_page_source_merged)
    # print(len(driver_page_source_merged))
    # print(driver_page_source)