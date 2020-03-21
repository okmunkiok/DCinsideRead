from . import common
import sys
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
# import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
from multiprocessing import Pool, freeze_support
from itertools import repeat
from itertools import product
from functools import partial
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# from urllib.request import urlopen

# from urllib.request import HTTPError
# from urllib.error import HTTPError
# from urllib.error import URLError

# import datetime
# import random
# random.seed(datetime.datetime.now())
# # !pip install lxml
# # !pip install psycopg2
# import psycopg2
# import string
# # print(string.ascii_letters)
# from datetime import datetime
# # import pandas as pd
# import multiprocessing
# # !pip install fake-useragent
# # fake-useragent는 속도가 매우 느리므로 가급적 쓰지 말 것
# # 다만 기존의 내 방식대로 생성된 header가 아닌 정식 header가 요구되는 사이트에서는 사용할 수도 있음
# # 허나 미리 여러 번 update해서 header들을 약 수십 개 만들어 놓고, 그것을 리스트에 넣는 것이 훨씬 나을 것으로 추정
# # https://pypi.org/project/fake-useragent/
# # !pip install selenium
# # https://pypi.org/project/selenium/
# import time
# now = time.localtime()
# import csv

gallery_list_dictionary = {
    "gallery_list_url": [
        "https://gall.dcinside.com/",
        "https://gall.dcinside.com/m"
    ],
    "gallery_url_regular_expression": [
        r"https?:\/\/gall.dcinside.com\/board\/lists\/\?id=\w*",
        r"https?:\/\/gall.dcinside.com\/mgallery\/board\/lists\/\?id=\w*"
    ],
    "gallery_tag_regular_expression": [
        r"\<\w*\s*\w*\s*\=\s*\"https?:\/\/gall.dcinside.com\/board\/lists\/\?id=\w*\"",
        r"\<\w*\s*\w*\s*\=\s*\"https?:\/\/gall.dcinside.com\/mgallery\/board\/lists\/\?id=\w*\""
    ],
}


# @common.print_log
def get_gallery_url_dictionary():
    gallery_url_dictionary = {}
    for i in range(len(gallery_list_dictionary["gallery_list_url"])):
        bs = common.get_bs_html_parsed(gallery_list_dictionary["gallery_list_url"][i])
        contents = bs.find_all("a", {"href": re.compile(gallery_list_dictionary["gallery_url_regular_expression"][i])})
        for content in contents:
            gallery_url_dictionary[content.text] = content.attrs["href"].replace("http:", "https:")
    return gallery_url_dictionary


# @common.print_log
def read_a_post_and_save_it_to_csv():
    pass


# @common.print_log
def read_post_reply_from_a_post(url, *args):
    regular_expression_for_extracting_post_number = r""
    regular_expression_for_extracting_reply_tag = r"comment_li_\w*"
    bs = common.get_bs_html_parsed(url)
    contents = bs.find_all("li", {"id": re.compile(regular_expression_for_extracting_reply_tag)})
    print(contents)
    pass


# @common.print_log
def get_post_number(content, *args):
    try:
        post_number_tag = content.find("td", class_="gall_num")
    except:
        return 0
    else:
        try:
            post_number = int(post_number_tag.text)
        except:
            return 0
        else:
            return post_number


# @common.print_log
def get_last_page_number(url, *args):
    try:
        regular_expression_for_getting_last_page_number = r"page=\w*"
        bs = common.get_bs_html_parsed(url)
        last_page_number_tag = bs.find("a", class_="page_end")
        match_list = common.get_match_list_by_regular_expression(regular_expression_for_getting_last_page_number,
                                                                 last_page_number_tag.attrs["href"])
        return int(match_list[0].split("=")[1])
    except:
        return 999999


# @common.print_log
def get_date(content, *args):
    date_tag = content.find("td", class_="gall_date")
    if date_tag is not None:
        try:
            date_raw = date_tag.attrs["title"]
        except:
            return 0
        else:
            return common.replace_several(date_raw, ["-", " ", ":"], "")
    else:
        return 0


# @common.print_log
def get_title(content, *args):
    # 일반 글
    title_tag_candidate = content.find("td", class_="gall_tit ub-word")
    if title_tag_candidate is not None:
        title_tag = title_tag_candidate.find("a")
        if title_tag is not None:
            return title_tag.text
    # 보이스 리플이 "본문"에 첨부된 글
    title_tag_candidate = content.find("td", class_="gall_tit ub-word voice_tit")
    if title_tag_candidate is not None:
        title_tag = title_tag_candidate.find("a")
        if title_tag is not None:
            return title_tag.text
    else:
        return 0


# @common.print_log
def get_writer(content, *args):
    writer_tag = content.find("td", class_="gall_writer ub-writer")
    if writer_tag is not None:
        try:
            writer = writer_tag.attrs["data-nick"]
        except:
            return 0
        else:
            return writer
    else:
        return 0


# @common.print_log
def get_ip(content, *args):
    ip_tag = content.find("td", class_="gall_writer ub-writer")
    if ip_tag is not None:
        try:
            ip_raw = ip_tag.attrs["data-ip"]
        except:
            return 0
        else:
            if ip_raw != "":
                return ip_raw.replace(".", "")
            else:
                return 0
    else:
        return 0


# @common.print_log
def get_view_count(content, *args):
    view_count_tag = content.find("td", class_="gall_count")
    if view_count_tag is not None:
        return view_count_tag.text
    else:
        return 0


# @common.print_log
def get_reply_number(content, *args):
    # 일반 글
    reply_number_tag_candidate = content.find("td", class_="gall_tit ub-word")
    if reply_number_tag_candidate is not None:
        reply_number_tag = reply_number_tag_candidate.find("a", class_="reply_numbox")
        if reply_number_tag is not None:
            return re.findall("\d+", reply_number_tag.text)[0]
    # 보이스 리플이 "본문"에 첨부된 글
    reply_number_tag_candidate = content.find("td", class_="gall_tit ub-word voice_tit")
    if reply_number_tag_candidate is not None:
        reply_number_tag = reply_number_tag_candidate.find("a", class_="reply_numbox")
        if reply_number_tag is not None:
            return re.findall("\d+", reply_number_tag.text)[0]
    else:
        return 0


# @common.print_log
def get_reply_all_html(reply_button_href_list=0, *args,
                       driver_page_source_list=[], driver, **kwargs):
    html = driver.page_source
    # driver_page_source = driver_page_source + html
    driver_page_source_list.append(html)
    bs = BeautifulSoup(html, "html.parser")
    # regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
    # contents = bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)})
    reply_button_tag = bs.find("div", class_="cmt_paging")
    if reply_button_tag is not None:
        reply_button_list = reply_button_tag.find_all("a")
    else:
        return
    # print(reply_button_list)
    reply_button_href_list = []
    for reply_button in reply_button_list:
        if reply_button.text not in ["처음", "이전", "다음", "끝"]:
            reply_button_href_list.append(reply_button.attrs["href"])

    for index, reply_button_href in enumerate(reply_button_href_list):
        whether_next = False
        condition1 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0) and \
                     (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) <= 15)
        condition2 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 14) and \
                     (30 >= int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) > 15)
        condition3 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0) and \
                     (45 >= int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) > 30)
        condition4 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 14) and \
                     (60 >= int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) > 45)
        condition = condition1 or condition2 or condition3 or condition4
        # condition |= (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 14)&\
        #              (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) > 15)
        if condition is not False:
            whether_next = True
        else:
            whether_next = False
        driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").click()

        html = driver.page_source
        driver_page_source_list.append(html)
        bs = BeautifulSoup(html, "html.parser")
        reply_button_tag = bs.find("div", class_="cmt_paging")
        reply_button_list = reply_button_tag.find_all("a")
        reply_button_href_list = []
        for reply_button in reply_button_list:
            if reply_button.text not in ["처음", "이전", "끝"]:
                reply_button_href_list.append(reply_button.attrs["href"])

        if whether_next:
            try:
                driver.find_element_by_xpath("//a[@href=\"" + reply_button_href_list[index + 1] + "\"]").click()
            except:
                return
            html = driver.page_source
            driver_page_source_list.append(html)
            bs = BeautifulSoup(html, "html.parser")
            reply_button_tag = bs.find("div", class_="cmt_paging")
            reply_button_list = reply_button_tag.find_all("a")
            reply_button_href_list = []
            for reply_button in reply_button_list:
                if reply_button.text not in ["처음", "이전", "끝"]:
                    reply_button_href_list.append(reply_button.attrs["href"])
            get_reply_all_html(reply_button_href_list, driver_page_source_list=driver_page_source_list, driver=driver)


# @common.print_log
def get_reply_date(content, *args):
    date_tag = content.find("span", class_="date_time")
    if date_tag is not None:
        date = common.replace_several(date_tag.text, [".", ":", " "], "")
        if len(date) < 14:
            date = str(datetime.today().year) + date
        return date
    else:
        return 0


# @common.print_log
def get_reply_title(content, *args):
    if content.find("span", class_="date_time") is not None:
        title_tag = content.find("p", class_="usertxt ub-word")
        if title_tag is not None:
            title = title_tag.text
        else:
            title = "(보이스 리플)"
        return title
    else:
        return 0


# @common.print_log
def get_reply_writer(content, *args):
    if content.find("span", class_="date_time") is not None:
        writer_tag = content.find("em")
        if writer_tag is not None:
            writer = writer_tag.text
        else:
            writer = 0
        return writer
    else:
        return 0


# @common.print_log
def get_reply_ip(content, *args):
    if content.find("span", class_="date_time") is not None:
        ip_tag = content.find("span", class_="ip")
        if ip_tag is not None:
            ip = ip_tag.text
        else:
            ip = 0
        return ip
    else:
        return 0


# @common.print_log
def get_reply(page_and_base_url_dictionary, *args,
              disable_gpu=True, headless=False,
              delete_legacy_temp_raw_data=True, delete_legacy_merged_data=True,
              pre_delete_all_legacy_raw_data=True,
              pre_delete_all_legacy_merged_data=True,
              multiprocessing=False,
              processes=8,
              # processes=16,
              get_reply_only=True, **kwargs):
    start_time = time.time()
    regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
    if pre_delete_all_legacy_raw_data:
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list=True)
        common.delete_all_legacy_data(delete_leagacy_temp_raw_data=delete_legacy_temp_raw_data, file_header=csv_header)
    if pre_delete_all_legacy_merged_data:
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list=True)
        common.delete_all_legacy_data(delete_legacy_merged_data=delete_legacy_merged_data, file_header=csv_header)

    read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary,
                                           print_save_message=True, post_list_dictionary={},
                                           delete_legacy_temp_raw_data=delete_legacy_temp_raw_data,
                                           delete_legacy_merged_data=delete_legacy_merged_data,
                                           read_post_and_save_it_to_csv=True,
                                           pre_delete_all_legacy_raw_data=pre_delete_all_legacy_raw_data,
                                           pre_delete_all_legacy_merged_data=pre_delete_all_legacy_merged_data,
                                           multi_processes_on=multiprocessing, multi_processes=processes,
                                           get_reply_only=get_reply_only)

    csv_file_path_name = merge_csv_files_for_each_gallery(page_and_base_url_dictionary, *args,
                                                          delete_leagacy_temp_raw_data=delete_legacy_temp_raw_data,
                                                          delete_legacy_merged_data=delete_legacy_merged_data,
                                                          read_post_list=True, read_post_content=False, read_post_reply=False,
                                                          get_reply_only=get_reply_only, **kwargs)

    csv = pd.read_csv(csv_file_path_name, index_col=0)

    post_url_list = csv["post_url"].values.tolist()

    for index, post_url in enumerate(post_url_list):
        if "&page" in post_url_list[index]:
            post_url_list[index] = post_url.replace("&page", "&t=cv&page")
        else:
            post_url_list[index] += "&t=cv"

    options = webdriver.ChromeOptions()
    if disable_gpu:
        options.add_argument("disable-gpu")
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    # driver2 = webdriver.Chrome(chrome_options=options)
    reply_dictionary = {}
    # print(post_url_list)
    for index, post_url in enumerate(post_url_list):
        # post_number = csv["post_number"].values[index]
        while 1:
            driver.get(post_url)
            if driver.page_source is not None:
                break

        driver_page_source_list = []
        # print(len(driver_page_source))
        # print(type(driver_page_source))
        # print(driver_page_source)
        get_reply_all_html(driver_page_source_list=driver_page_source_list, driver=driver)
        # driver_page_source_merged = "".join(driver_page_source)
        # date_list = []
        for driver_page_source in driver_page_source_list:
            bs = BeautifulSoup(driver_page_source, "html.parser")
            regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
            contents = bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)})
            # print(type(contents))
            regular_expression_for_getting_reply = r"reply_li_[^0]\w*"
            contents.extend(bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)}))

            for content in contents:
                reply_dictionary[len(reply_dictionary)] = {
                    "post_number": csv["post_number"].values[index],
                    "date": get_reply_date(content),
                    "title": get_reply_title(content),
                    "writer": get_reply_writer(content),
                    "ip": get_reply_ip(content)
                }

        df = pd.DataFrame(reply_dictionary).transpose()
        csv_path_and_name = get_csv_path_and_name(
            common.get_directories_dictionary("dcinside")["temp_raw_data_path"], page_and_base_url_dictionary,
            post_number_from=csv["post_number"].values.min(), post_number_to=csv["post_number"].values.max(),
            read_post_reply=True)
        df.to_csv(csv_path_and_name)
        reply_dictionary.clear()

    merge_csv_files_for_each_gallery(page_and_base_url_dictionary,
                                     delete_leagacy_temp_raw_data=delete_legacy_temp_raw_data,
                                     delete_legacy_merged_data=delete_legacy_merged_data,
                                     read_post_list=False, read_post_content=False, read_post_reply=True,
                                     get_reply_only=get_reply_only)

    driver.close()
    print("%.2f초 걸렸다" % (time.time() - start_time))
    return


# @common.print_log
def get_page_and_base_url_dictionary(gallery_name="클래식", whether_recommended_only=False, *args):
    page_and_base_url_dictionary = {
        "start_page": 1,
        "last_page": 1,
        "url": gallery_url_dictionary[gallery_name],
        "base_url": gallery_url_dictionary[gallery_name] + "&page=",
        "post_base_url": "",
        "save_csv_page_unit": 100,
        "temp_raw_data_path": common.get_directories_dictionary("dcinside")["temp_raw_data_path"],
        "merged_data_path": common.get_directories_dictionary("dcinside")["merged_data_path"],
        "post_list_column_data_types": {
            "post_number": "int64",
            "date": "int64",
            "title": "object",
            "writer": "object",
            "ip": "int64",
            "view_count": "int64",
            "reply_number": "int64",
            "post_url": "object"
        },
        "whether_recommended_only": whether_recommended_only
    }
    if whether_recommended_only == "개념글":
        page_and_base_url_dictionary["last_page"] = get_last_page_number(page_and_base_url_dictionary["url"]
                                                                         + "&exception_mode=recommend")
    else:
        page_and_base_url_dictionary["last_page"] = get_last_page_number(page_and_base_url_dictionary["url"])
    if whether_recommended_only == "개념글":
        page_and_base_url_dictionary["whether_recommended_only"] = True
    # if whether_recommended_only:
    #     pass
    # else:
    page_and_base_url_dictionary["post_base_url"] = str(
        page_and_base_url_dictionary["url"].replace("lists", "view")) + "&no="
    return page_and_base_url_dictionary


# @common.print_log
def get_url_list(page_and_base_url_dictionary, *args):
    url_list = [
        page_and_base_url_dictionary["base_url"]
        + str(i) for i in range(
            page_and_base_url_dictionary["start_page"],
            page_and_base_url_dictionary["last_page"] + 1)]
    url_list_of_recommended = []
    if page_and_base_url_dictionary["whether_recommended_only"]:
        for url in url_list:
            url_list_of_recommended.append(url + "&exception_mode=recommend")
        return url_list_of_recommended
    return url_list


# @common.print_log
def read_a_list_of_posts_and_save_it_to_dictionary(url, *args,
                                                   post_list_dictionary={}, page_and_base_url_dictionary,
                                                   print_save_message=True, **kwargs):
    limit_iterate_for_unexpected_error = 10
    # 오류가 왜 발생하는지 도통 분석이 안 되니, 일단 고육지책으로 최대 n번까지 다시 시도하게 하였음
    # 이렇게 하지 않으면 에러 났다고 메시지만 내고 그냥 넘어가서 빼먹는 게시물이 발생함
    # 물론 n번 시도를 연속으로 실패하면 이렇게 해도 빼먹는 게시물은 나오겠지만, 가능성은 아주 아주 작게 된 것이 의미 있는 지점.
    # 대충 체감상 20% 이상의 확률로 발생하던 것이 1%보다 훨씬 작게 되는 것 같음.
    # 이론적으로나 발생 가능하다는 거지, 사실상 0%에 가깝다 보아도 큰 문제 없다고 본다
    start_time = time.time()
    for i in range(limit_iterate_for_unexpected_error):
        try:
            bs = common.get_bs_html_parsed(url)
            contents = bs.find("tbody").find_all("tr")  # except 메시지로 보아 여기서 뭔가 알 수 없는 에러가 나는 것 같음
            if contents is None:
                print("There was no content. Jump to next page")
                return
            # max_post_number = 0
            min_post_number = 0
            for content in contents:
                if page_and_base_url_dictionary["whether_recommended_only"]:
                    post_list_dictionary[len(post_list_dictionary)] = {
                        "post_number": get_post_number(content),
                        "date": get_date(content),
                        "title": get_title(content),
                        "writer": get_writer(content),
                        "ip": get_ip(content),
                        "view_count": get_view_count(content),
                        "reply_number": get_reply_number(content),
                        "post_url": page_and_base_url_dictionary["post_base_url"] + str(get_post_number(content)) + "&exception_mode=recommend"
                    }
                else:
                    post_list_dictionary[len(post_list_dictionary)] = {
                        "post_number": get_post_number(content),
                        "date": get_date(content),
                        "title": get_title(content),
                        "writer": get_writer(content),
                        "ip": get_ip(content),
                        "view_count": get_view_count(content),
                        "reply_number": get_reply_number(content),
                        "post_url": page_and_base_url_dictionary["post_base_url"] + str(get_post_number(content))
                    }
            min_post_number = get_post_number(content)
            df = pd.DataFrame(post_list_dictionary).transpose()
            csv_path_and_name = get_csv_path_and_name(
                common.get_directories_dictionary("dcinside")["temp_raw_data_path"], page_and_base_url_dictionary,
                post_number_from=df["post_number"].values.min(), post_number_to=df["post_number"].values.max(), read_post_list=True)
            df.to_csv(csv_path_and_name)
            # intermediate_check_page = current_page[index] + 1
            post_list_dictionary.clear()
            if print_save_message:
                print(csv_path_and_name)
                print("저장하는 데 %.2f초 걸렸다" % (time.time() - start_time))
            # print(post_list_dictionary)
            return
        except:
            continue


# @common.print_log
def get_csv_header(page_and_base_url_dictionary, *args,
                   read_post_list=False, read_post_content=False, read_post_reply=False, **kwargs):
    regular_expression_for_csv_name_header = r"id=\w*"
    match_list = common.get_match_list_by_regular_expression(regular_expression_for_csv_name_header,
                                                             page_and_base_url_dictionary["url"])
    header_candidate = match_list[0].split("=")[1] + "_"
    if page_and_base_url_dictionary["whether_recommended_only"]:
        header_candidate += "recommended "
    if read_post_list:
        return header_candidate + "post list"
    if read_post_content:
        return header_candidate + "post content"
    if read_post_reply:
        return header_candidate + "post reply"


# @common.print_log
def get_csv_path_and_name(path, page_and_base_url_dictionary, *args,
                          post_number_from=0, post_number_to=0, raw_or_not_that_is_merged=True,
                          read_post_list=False, read_post_content=False, read_post_reply=False, **kwargs):
    if raw_or_not_that_is_merged:
        csv_path_and_name = (
                common.get_directories_dictionary("dcinside")["temp_raw_data_path"]
                + get_csv_header(page_and_base_url_dictionary, read_post_list=read_post_list,
                                 read_post_content=read_post_content, read_post_reply=read_post_reply)
                + " post_number from " + str(post_number_from) + " to " + str(post_number_to)
                + " " + datetime.now().strftime("%Y%m%d%H%M%S")
                + ".csv"
        )
        return csv_path_and_name
    else:
        csv_path_and_name = (
                common.get_directories_dictionary("dcinside")["merged_data_path"]
                + get_csv_header(page_and_base_url_dictionary, read_post_list=read_post_list,
                                 read_post_content=read_post_content, read_post_reply=read_post_reply)
                + " " + datetime.now().strftime("%Y%m%d%H%M%S")
                + ".csv"
        )
        return csv_path_and_name


# @common.print_log
def merge_csv_files_for_each_gallery(page_and_base_url_dictionary, *args,
                                     delete_leagacy_temp_raw_data=False, delete_legacy_merged_data=False,
                                     read_post_list=False, read_post_content=False, read_post_reply=False,
                                     get_reply_only=False, **kwargs):
    start_time = time.time()
    csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list=read_post_list,
                                read_post_content=read_post_content, read_post_reply=read_post_reply)
    csv_file_list = []
    for file_name in os.listdir(page_and_base_url_dictionary["temp_raw_data_path"]):
        if csv_header in file_name:
            csv_file_list.append(file_name)

    dataframe_list = []
    for csv_file in csv_file_list[::-1]:
        csv = pd.read_csv(page_and_base_url_dictionary["temp_raw_data_path"] + csv_file, index_col=0)
        # csv = pd.read_csv(page_and_base_url_dictionary["temp_raw_data_path"] + csv_file, index_col=1)
        dataframe_list.append(pd.DataFrame(csv))

    csv_file_list = []
    for file_name in os.listdir(page_and_base_url_dictionary["merged_data_path"]):
        if csv_header in file_name:
            csv_file_list.append(file_name)

    # if not get_reply_only:
    for csv_file in csv_file_list[::-1]:
        csv = pd.read_csv(page_and_base_url_dictionary["merged_data_path"] + csv_file, index_col=0)
        # csv = pd.read_csv(page_and_base_url_dictionary["merged_data_path"] + csv_file, index_col=1)
        dataframe_list.append(pd.DataFrame(csv))
    common.delete_all_legacy_data(delete_leagacy_temp_raw_data=delete_leagacy_temp_raw_data, file_header=csv_header)
    common.delete_all_legacy_data(delete_legacy_merged_data=delete_legacy_merged_data, file_header=csv_header)

    merged_dataframe = pd.concat(dataframe_list, sort=False).drop_duplicates(["title"], keep="first")
    merged_dataframe = merged_dataframe.sort_values(by=["post_number"], axis=0, ascending=False)
    merged_dataframe = merged_dataframe[merged_dataframe["post_number"] != 0]
    # merged_dataframe = merged_dataframe.reset_index(drop=False, inplace=False)
    # merged_dataframe = merged_dataframe.reset_index()
    # merged_dataframe["0"] = np.arange(len(merged_dataframe["0"]))
    # print(merged_dataframe["Unnamed: 0"])
    # print(merged_dataframe.head())
    # print(merged_dataframe.iloc[0])
    if read_post_reply:
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_reply=True)
        common.delete_all_legacy_data(delete_leagacy_temp_raw_data=delete_leagacy_temp_raw_data, file_header=csv_header)
        common.delete_all_legacy_data(delete_legacy_merged_data=delete_legacy_merged_data, file_header=csv_header)
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list=True)
        common.delete_all_legacy_data(delete_legacy_merged_data=delete_legacy_merged_data, file_header=csv_header)

    csv_path_and_name = get_csv_path_and_name(page_and_base_url_dictionary["merged_data_path"],
                                                  page_and_base_url_dictionary, raw_or_not_that_is_merged=False,
                                                  read_post_list=read_post_list,
                                                  read_post_content=read_post_content,
                                                  read_post_reply=read_post_reply)
    merged_dataframe.to_csv(csv_path_and_name)
    # csv_temp = pd.read_csv(csv_path_and_name, index_col=0)
    # csv_temp = pd.read_csv(csv_path_and_name, index_col=1)
    # print(csv_temp.head())
    # csv_temp[""] = np.arange(len(csv_temp[""]))
    # csv_temp["0"] = np.arange(len(csv_temp["0"]))
    # csv_temp["Unnamed: 0"] = np.arange(len(csv_temp["Unnamed: 0"]))


    # csv_temp.to_csv(csv_path_and_name)
    # csv = csv_temp.reset_index()
    # csv.to_csv(csv_path_and_name)
    print(get_csv_path_and_name(page_and_base_url_dictionary["merged_data_path"],
                                page_and_base_url_dictionary, raw_or_not_that_is_merged=False,
                                read_post_list=read_post_list, read_post_content=read_post_content,
                                read_post_reply=read_post_reply))
    print("저장하는 데 %.2f초 걸렸다" % (time.time() - start_time))
    return csv_path_and_name
    # return (get_csv_path_and_name(page_and_base_url_dictionary["merged_data_path"],
    #                             page_and_base_url_dictionary, raw_or_not_that_is_merged=False,
    #                             read_post_list=read_post_list, read_post_content=read_post_content,
    #                             read_post_reply=read_post_reply))


# @common.print_log
def read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary, *args,
                                           print_save_message=True, post_list_dictionary={},
                                           delete_legacy_temp_raw_data=True, delete_legacy_merged_data=True,
                                           read_post_and_save_it_to_csv=True,
                                           pre_delete_all_legacy_raw_data=False,
                                           pre_delete_all_legacy_merged_data=False,
                                           multiprocessing=False,
                                           # processes=4,
                                           processes=8,
                                           # processes=16, # 유선 랜에서는 이게 더 빠르더라
                                           get_reply_only=False, **kwargs):
    if pre_delete_all_legacy_raw_data:
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list=True)
        common.delete_all_legacy_data(delete_leagacy_temp_raw_data=delete_legacy_temp_raw_data, file_header=csv_header)
    if pre_delete_all_legacy_merged_data:
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list=True)
        common.delete_all_legacy_data(delete_legacy_merged_data=delete_legacy_merged_data, file_header=csv_header)


    start_time = time.time()

    if multiprocessing:
        freeze_support()
        pool = Pool(processes=processes)
        pool.map(partial(read_a_list_of_posts_and_save_it_to_dictionary,
                         page_and_base_url_dictionary=page_and_base_url_dictionary),
                 get_url_list(page_and_base_url_dictionary))
        pool.close()
    else:
        for url in get_url_list(page_and_base_url_dictionary):
            read_a_list_of_posts_and_save_it_to_dictionary(url,
                                                           page_and_base_url_dictionary=page_and_base_url_dictionary)

    merge_csv_files_for_each_gallery(page_and_base_url_dictionary,
                                     delete_leagacy_temp_raw_data=delete_legacy_temp_raw_data,
                                     delete_legacy_merged_data=delete_legacy_merged_data,
                                     read_post_list=True, read_post_content=False, read_post_reply=False,
                                     get_reply_only=get_reply_only)


if __name__ == "__main__":
    pass

# 아래는 필요한 변수들 미리 저장한 것 (이 문서 내의 함수들을 사용)
# 얘네들은 처음 호출할 때 딱 한 번만 가동되고, 이후에는 계속 저장된 값을 활용하는 것으로 추정됨
# 처음에 얘가 함수 호출하는 것 때문에 최대 5~10초 정도 걸린다. 이후에는 0
gallery_url_dictionary = get_gallery_url_dictionary()
