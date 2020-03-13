import DCinsideRead

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from . import common
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import inspect
from datetime import datetime
import time

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


def get_gallery_url_dictionary():
    try:
        gallery_url_dictionary = {}
        for i in range(len(gallery_list_dictionary["gallery_list_url"])):
            bs = common.get_bs_html_parsed(gallery_list_dictionary["gallery_list_url"][i])
            contents = bs.find_all("a", {"href": re.compile(gallery_list_dictionary["gallery_url_regular_expression"][i])})
            for content in contents:
                gallery_url_dictionary[content.text] = content.attrs["href"]
        return gallery_url_dictionary
    except:
        common.print_error(inspect.currentframe())

def read_a_post_and_save_it_to_csv():
    pass

def read_post_reply_from_a_post(url):
    regular_expression_for_extracting_post_number = r""
    regular_expression_for_extracting_reply_tag = r"comment_li_\w*"
    bs = common.get_bs_html_parsed(url)
    contents = bs.find_all("li", {"id": re.compile(regular_expression_for_extracting_reply_tag)})
    print(contents)
    pass

def get_post_number(content):
    try:
        try:
            post_number_tag = content.find("td", class_ = "gall_num")
        except:
            return 0
        else:
            try:
                post_number = int(post_number_tag.text)
            except:
                return 0
            else:
                return post_number
    except:
        common.print_error(inspect.currentframe())

def get_last_page_number(url):
    try:
        try:
            regular_expression_for_getting_last_page_number = r"page=\w*"
            bs = common.get_bs_html_parsed(url)
            last_page_number_tag = bs.find("a", class_ = "page_end")
            match_list = common.get_match_list_by_regular_expression(regular_expression_for_getting_last_page_number, last_page_number_tag.attrs["href"])
            return int(match_list[0].split("=")[1])
        except:
            return 999999
    except:
        common.print_error(inspect.currentframe())

def get_date(content):
    try:
        date_tag = content.find("td", class_ = "gall_date")
        if date_tag != None:
            try:
                date_raw = date_tag.attrs["title"]
            except:
                return 0
            else:
                return common.replace_several(date_raw, ["-", " ", ":"], "")
        else:
            return 0
    except:
        common.print_error(inspect.currentframe())

def get_title(content):
    try:
        # 일반 글
        title_tag_candidate = content.find("td", class_ = "gall_tit ub-word")
        if title_tag_candidate != None:
            title_tag = title_tag_candidate.find("a")
            if title_tag != None:
                return title_tag.text
        # 보이스 리플이 "본문"에 첨부된 글
        title_tag_candidate = content.find("td", class_ = "gall_tit ub-word voice_tit")
        if title_tag_candidate != None:
            title_tag = title_tag_candidate.find("a")
            if title_tag != None:
                return title_tag.text
        else:
            return 0
    except:
        common.print_error(inspect.currentframe())

def get_writer(content):
    try:
        writer_tag = content.find("td", class_ = "gall_writer ub-writer")
        if writer_tag != None:
            try:
                writer = writer_tag.attrs["data-nick"]
            except:
                return 0
            else:
                return writer
        else:
            return 0
    except:
        common.print_error(inspect.currentframe())

def get_ip(content):
    try:
        ip_tag = content.find("td", class_ = "gall_writer ub-writer")
        if ip_tag != None:
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
    except:
        common.print_error(inspect.currentframe())

def get_view_count(content):
    try:
        view_count_tag = content.find("td", class_ = "gall_count")
        if view_count_tag != None:
            return view_count_tag.text
        else:
            return 0
    except:
        common.print_error(inspect.currentframe())

def get_reply_number(content):
    try:
        # 일반 글
        reply_number_tag_candidate = content.find("td", class_ = "gall_tit ub-word")
        if reply_number_tag_candidate != None:
            reply_number_tag = reply_number_tag_candidate.find("a", class_ = "reply_numbox")
            if reply_number_tag != None:
                return re.findall("\d+", reply_number_tag.text)[0]
        # 보이스 리플이 "본문"에 첨부된 글
        reply_number_tag_candidate = content.find("td", class_ = "gall_tit ub-word voice_tit")
        if reply_number_tag_candidate != None:
            reply_number_tag = reply_number_tag_candidate.find("a", class_ = "reply_numbox")
            if reply_number_tag != None:
                return re.findall("\d+", reply_number_tag.text)[0]
        else:
            return 0
    except:
        common.print_error(inspect.currentframe())

def get_reply(content):
    try:
        return
    except:
        common.print_error(inspect.currentframe())

def get_page_and_base_url_dictionary(gallery_name = "클래식"):
    try:
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
            }
        }
        page_and_base_url_dictionary["post_base_url"] = str(page_and_base_url_dictionary["url"].replace("lists", "view")) + "&no="
        return page_and_base_url_dictionary
    except:
        common.print_error(inspect.currentframe())

def get_url_list(page_and_base_url_dictionary):
    try:
        url_list = [
            page_and_base_url_dictionary["base_url"]
            + str(i) for i in range(
                page_and_base_url_dictionary["start_page"],
                page_and_base_url_dictionary["last_page"] + 1)]
        return url_list
    except:
        common.print_error(inspect.currentframe())
    
def read_a_list_of_posts_and_save_it_to_dictionary(url, post_list_dictionary, page_and_base_url_dictionary):
    limit_iterate_for_unexpected_error = 20
    # 오류가 왜 발생하는지 도통 분석이 안 되니, 일단 고육지책으로 최대 n번까지 다시 시도하게 하였음
    # 이렇게 하지 않으면 에러 났다고 메시지만 내고 그냥 넘어가서 빼먹는 게시물이 발생함
    # 물론 n번 시도를 연속으로 실패하면 이렇게 해도 빼먹는 게시물은 나오겠지만, 가능성은 아주 아주 작게 된 것이 의미 있는 지점.
    # 대충 체감상 20% 이상의 확률로 발생하던 것이 1%보다 훨씬 작게 되는 것 같음.
    # 이론적으로나 발생 가능하다는 거지, 사실상 0%에 가깝다 보아도 큰 문제 없다고 본다
    try:
        for i in range(limit_iterate_for_unexpected_error):
            try:
                bs = common.get_bs_html_parsed(url)
                contents = bs.find("tbody").find_all("tr") # except 메시지로 보아 여기서 뭔가 알 수 없는 에러가 나는 것 같음
                if contents == None:
                    print("There was no content. Jump to next page")
                    return
                for content in contents:
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
                return
            except:
                continue
            
    except:
        common.print_error(inspect.currentframe())

def get_csv_header(page_and_base_url_dictionary, read_post_list = False, read_post_content = False, read_post_reply = False):
    try:
        regular_expression_for_csv_name_header = r"id=\w*"
        match_list = common.get_match_list_by_regular_expression(regular_expression_for_csv_name_header, page_and_base_url_dictionary["url"])
        header_candidate = match_list[0].split("=")[1] + "_"
        if read_post_list == True:
            return header_candidate + "post list"
        if read_post_content == True:
            return header_candidate + "post content"
        if read_post_reply == True:
            return header_candidate + "post reply"
    except:
        common.print_error(inspect.currentframe())

def get_csv_path_and_name(path, page_and_base_url_dictionary, page_from = 0, page_to = 0, raw_or_not_that_is_merged = True,\
    read_post_list = False, read_post_content = False, read_post_reply = False):
    try:
        if raw_or_not_that_is_merged == True:
            csv_path_and_name = (
                common.get_directories_dictionary("dcinside")["temp_raw_data_path"]
                + get_csv_header(page_and_base_url_dictionary, read_post_list = read_post_list, read_post_content = read_post_content, read_post_reply = read_post_reply)
                + " page from " + str(page_from) + " to " + str(page_to)
                + " " + datetime.now().strftime("%Y%m%d%H%M%S")
                + ".csv"
            )
            return csv_path_and_name
        else:
            csv_path_and_name = (
                common.get_directories_dictionary("dcinside")["merged_data_path"]
                + get_csv_header(page_and_base_url_dictionary, read_post_list = read_post_list, read_post_content = read_post_content, read_post_reply = read_post_reply)
                + " " + datetime.now().strftime("%Y%m%d%H%M%S")
                + ".csv"
            )
            return csv_path_and_name
    except:
        common.print_error(inspect.currentframe())

def merge_csv_files_for_each_gallery(page_and_base_url_dictionary, delete_leagacy_temp_raw_data = False, delete_legacy_merged_data = False,\
    read_post_list = False, read_post_content = False, read_post_reply = False):
    try:
        start_time = time.time()
        csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list = read_post_list, read_post_content = read_post_content, read_post_reply = read_post_reply)
        csv_file_list = []
        for file_name in os.listdir(page_and_base_url_dictionary["temp_raw_data_path"]):
            if csv_header in file_name:
                csv_file_list.append(file_name)
        
        dataframe_list = []
        for csv_file in csv_file_list[::-1]:
            csv = pd.read_csv(page_and_base_url_dictionary["temp_raw_data_path"] + csv_file, index_col = 0)
            dataframe_list.append(pd.DataFrame(csv))
        
        csv_file_list = []
        for file_name in os.listdir(page_and_base_url_dictionary["merged_data_path"]):
            if csv_header in file_name:
                csv_file_list.append(file_name)
        
        for csv_file in csv_file_list[::-1]:
            csv = pd.read_csv(page_and_base_url_dictionary["merged_data_path"] + csv_file, index_col = 0)
            dataframe_list.append(pd.DataFrame(csv))

        common.delete_all_legacy_data(delete_leagacy_temp_raw_data = delete_leagacy_temp_raw_data, file_header = csv_header)
        common.delete_all_legacy_data(delete_legacy_merged_data = delete_legacy_merged_data, file_header = csv_header)

        merged_dataframe = pd.concat(dataframe_list, sort = False).drop_duplicates(["post_number"], keep = "first")
        merged_dataframe.to_csv(get_csv_path_and_name(page_and_base_url_dictionary["merged_data_path"],\
            page_and_base_url_dictionary, raw_or_not_that_is_merged = False, read_post_list = read_post_list, read_post_content = read_post_content, read_post_reply = read_post_reply))
        print(get_csv_path_and_name(page_and_base_url_dictionary["merged_data_path"],\
            page_and_base_url_dictionary, raw_or_not_that_is_merged = False, read_post_list = read_post_list, read_post_content = read_post_content, read_post_reply = read_post_reply))
        print("방금 파일을 저장하는 데 %.2f초 걸렸다" % (time.time() - start_time))
        print("프로그램을 시작하고 지금까지 총 %.2f초 걸렸다" % (time.time() - DCinsideRead_dcinside_start_time))
    except:
        common.print_error(inspect.currentframe())

def read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary, print_elapsed_time_per_save_csv_page_unit = True,\
    print_save_message = True, delete_leagacy_temp_raw_data = False, delete_legacy_merged_data = False, read_post_and_save_it_to_csv = True,\
    pre_delete_all_leagcy_data_or_not = False):
    try:
        if pre_delete_all_leagcy_data_or_not == True:
            csv_header = get_csv_header(page_and_base_url_dictionary, read_post_list = True)
            common.delete_all_legacy_data(delete_leagacy_temp_raw_data = True, file_header = csv_header)
            common.delete_all_legacy_data(delete_legacy_merged_data = True, file_header = csv_header)

        current_page = [
            i for i in range(
                page_and_base_url_dictionary["start_page"],
                page_and_base_url_dictionary["last_page"] + 1)]
        last_page = page_and_base_url_dictionary["last_page"]
        save_csv_page_unit = page_and_base_url_dictionary["save_csv_page_unit"]
        intermediate_check_page = page_and_base_url_dictionary["start_page"]
        post_list_dictionary = {}

        start_time = time.time()
        for index, url in enumerate(get_url_list(page_and_base_url_dictionary)):   
            read_a_list_of_posts_and_save_it_to_dictionary(url, post_list_dictionary, page_and_base_url_dictionary)
            if (last_page - current_page[index]) % save_csv_page_unit == 0:
                df = pd.DataFrame(post_list_dictionary).transpose()
                csv_path_and_name = get_csv_path_and_name(common.get_directories_dictionary("dcinside")["temp_raw_data_path"],\
                    page_and_base_url_dictionary, intermediate_check_page, current_page[index], read_post_list = True)
                df.to_csv(csv_path_and_name)
                intermediate_check_page = current_page[index] + 1
                post_list_dictionary.clear()
                if print_save_message == True:
                    print(csv_path_and_name)
                if print_elapsed_time_per_save_csv_page_unit == True:
                    print("방금 파일을 저장하는 데 %.2f초 걸렸다" % (time.time() - start_time))
                    print("프로그램을 시작하고 지금까지 총 %.2f초 걸렸다" % (time.time() - DCinsideRead_dcinside_start_time))
                start_time = time.time()

        merge_csv_files_for_each_gallery(page_and_base_url_dictionary,\
            delete_leagacy_temp_raw_data = delete_leagacy_temp_raw_data,\
            delete_legacy_merged_data = delete_legacy_merged_data,
            read_post_list = True, read_post_content = False, read_post_reply = False)
    except:
        common.print_error(inspect.currentframe())


if __name__ == "__main__":
    pass

# 아래는 필요한 변수들 미리 저장한 것 (이 문서 내의 함수들을 사용)
# 얘네들은 처음 호출할 때 딱 한 번만 가동되고, 이후에는 계속 저장된 값을 활용하는 것으로 추정됨
# 처음에 얘가 함수 호출하는 것 때문에 최대 5~10초 정도 걸린다. 이후에는 0
DCinsideRead_dcinside_start_time = time.time()
gallery_url_dictionary = get_gallery_url_dictionary()


