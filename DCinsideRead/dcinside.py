import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from . import common
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import pandas as pd


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




def update_gallery_url_dictionary(url_info_dictionary):
    try:
        req = common.requests_get(url_info_dictionary["gallery_list_url"])
        pattern = re.compile(url_info_dictionary["gallery_tag_regular_expression"])
        match_list = re.findall(pattern, req.text)
        tag_list = []
        for match_one in match_list:
            i = re.sub("[\n\t\r<\"]", "", match_one)
            temp_list = []
            temp = re.split("[\s*]", " ".join(i.split()))
            # <a  href="http://gall.dcinside.com/mgallery/board/lists/?id=lovelyviolin"
            # 위의 split은 a와 href 사이의 여러 공백을 1개로 만들어 주지만, 이하 다른 부분들에서 공백이 생기면 문제가 된다
            # 아직은 그렇게 되어 있지 않으니 (내가 지금 문법을 숙지하지 못해서 그런데, 문법상 아예 발생하지 않는 경우일 수도 있음), 그건 나중에 문제가 되면 해결하자
            temp_list.append(temp[0])
            temp_list.append(re.split("=", temp[1], 1))
            tag_list.append(temp_list)
        req = common.urllib_request_Request(url_info_dictionary["gallery_list_url"])
        html = urllib.request.urlopen(req)
        bs = BeautifulSoup(html, "html.parser")
        gallery_url_dictionary = {}
        # for i in range(10): # for fast test
        for i in range(len(tag_list)):
            gallery_url_dictionary[len(gallery_url_dictionary)] = {
                "gallery_name": bs.find(tag_list[i][0], {tag_list[i][1][0]: tag_list[i][1][1].replace("\"", "")}).text,
                "gallery_url": tag_list[i][1][1].replace("\"", "")
            }
        return gallery_url_dictionary
    except:
        print("error on function wlt.dcinside.update_gallery_url_dictionary()")

def get_gallery_url_dictionary(*update_or_not):
    try:
        if len(update_or_not) == 0:
            update_or_not = False
        else:
            update_or_not = update_or_not[0]
        gallery_url_info = {
            "gallery_list_url": "https://gall.dcinside.com/",
            "gallery_url_regular_expression": r"https?:\/\/gall.dcinside.com\/board\/lists\/\?id=\w*",
            "gallery_tag_regular_expression": r"\<\w*\s*\w*\s*\=\s*\"https?:\/\/gall.dcinside.com\/board\/lists\/\?id=\w*\""
            }
        
        minor_gallery_url_info = {
            "gallery_list_url": "https://gall.dcinside.com/m",
            "gallery_url_regular_expression": r"https?:\/\/gall.dcinside.com\/mgallery\/board\/lists\/\?id=\w*",
            "gallery_tag_regular_expression": r"\<\w*\s*\w*\s*\=\s*\"https?:\/\/gall.dcinside.com\/mgallery\/board\/lists\/\?id=\w*\""
        }
        community_name = "dcinside"
        gallery_url_list_csv_file_name_format ={
                "head": "gallery_url_dictionary_made_",
                "tail": ".csv"
            }
        directory_info_dictionary = common.check_and_make_data_directories(community_name)
        csv_file_name = gallery_url_list_csv_file_name_format["head"] + gallery_url_list_csv_file_name_format["tail"]
        csv_file_path_and_name = directory_info_dictionary["url_list_path"] + csv_file_name
        try:
            does_list_csv_exist_or_not = False
            does_list_csv_path_exist_or_not = False
            list_for_checking_url_list_csv_exists = os.listdir(directory_info_dictionary["url_list_path"])
            does_list_csv_path_exist_or_not = True
            for element in list_for_checking_url_list_csv_exists:
                if csv_file_name == element:
                    does_list_csv_exist_or_not = True
                    break
        except:
            csv_file_path_and_name = update_gallery_url_dictionary()
            does_list_csv_path_exist_or_not = False
        if update_or_not == True or does_list_csv_path_exist_or_not == False or does_list_csv_exist_or_not == False:
            gallery_url_dictionary = update_gallery_url_dictionary(gallery_url_info)
            df1 = pd.DataFrame(gallery_url_dictionary).transpose()
            minor_gallery_url_dictionary = update_gallery_url_dictionary(minor_gallery_url_info)
            # 마이너 갤러리 순위권에 있는 애들은 글씨에 색이 입혀져 있어서 기존 regular expression으로 포섭이 되지 않음
            # ex. 중세게임 마이너 갤러리 등
            # 나중에 처리하겠음. 일단은 패스
            df2 = pd.DataFrame(minor_gallery_url_dictionary).transpose()
            df = df1.append(df2, ignore_index = True)
            df = df.drop_duplicates(subset = [list(gallery_url_dictionary[0].keys())[0]], keep = "first").reset_index(drop = True)
            df.to_csv(csv_file_path_and_name)
        df = pd.read_csv(csv_file_path_and_name, index_col = 0)
        gallery_url_dictionary = df.set_index("gallery_name")["gallery_url"].to_dict()
        return gallery_url_dictionary
    except:
        print("error on function wlt.dcinside.get_gallery_url_dictionary()")

def request_and_get_bs_objects(url):
    try:
        try:
            req = common.urllib_request_Request(url)
            html = urllib.request.urlopen(req)
            bs = BeautifulSoup(html, "html.parser")
            contents = bs.find("tbody").find_all("tr")
        except:
            print("error on function wlt.dcinside.request_and_get_bs_objects()")
        else:
            return contents
    except:
        print("error on function wlt.dcinside.request_and_get_bs_objects()")

def get_post_number(content):
    try:
        try:
            post_number = content.attrs["data-no"]
        except:
            return 0
        else:
            return post_number
    except:
        print("error on function wlt.dcinside.get_post_number()")

def get_date(content):
    try:
        date_tag = content.find("td", class_ = "gall_date")
        if date_tag != None:
            try:
                date_raw = date_tag.attrs["title"]
            except:
                return 0
            else:
                return date_raw.replace("-", "")
        else:
            return 0
    except:
        print("error on function wlt.dcinside.get_date()")

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
        print("error on function wlt.dcinside.get_title()")

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
        print("error on function wlt.dcinside.get_title()")

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
        print("error on function wlt.dcinside.get_writer()")

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
        print("error on function wlt.dcinside.get_ip()")

def get_view_count(content):
    try:
        view_count_tag = content.find("td", class_ = "gall_count")
        if view_count_tag != None:
            return view_count_tag.text
        else:
            return 0
    except:
        print("error on function wlt.dcinside.get_view_count()")

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
        print("error on function wlt.dcinside.get_reply_number()")

def get_page_and_base_url_dictionary(url):
    try:
        page_and_base_url_dictionary = {
            "start_page": 1,
            "last_page": 1,
            "base_url": url + "&page=",
            "save_dict_page_unit": 10,
            "save_csv_page_unit": 10,
            "column_data_types": {
                "post_number": "int64",
                "date": "object",
                "title": "object",
                "writer": "object",
                "ip": "int64",
                "view_count": "int64",
                "reply_number": "int64"
            }
        }
        return page_and_base_url_dictionary
    except:
        print("error on function wlt.dcinside.get_page_and_base_url_dictionary()")

def get_url_list(page_and_base_url_dictionary):
    try:
        url_list = [
            page_and_base_url_dictionary["base_url"]
            + str(i) for i in range(
                page_and_base_url_dictionary["start_page"],
                page_and_base_url_dictionary["last_page"] + 1)]
        return url_list
    except:
        print("error on function wlt.dcinside.get_url_list()")
    
def read_a_list_of_posts_and_save_it_to_dictionary(url, contents_dict):
    try:
        contents = request_and_get_bs_objects(url)
        if contents == None:
            print("There was no content. Jump to next page")
            return
        for content in contents:
            contents_dict[len(contents_dict)] = {
                "post_number": get_post_number(content),
                "date": get_date(content),
                "title": get_title(content),
                "writer": get_writer(content),
                "ip": get_ip(content),
                "view_count": get_view_count(content),
                "reply_number": get_reply_number(content)
            }
        return
    except:
        print("error on function wlt.dcinside.read_a_list_of_posts_and_save_it_to_dictionary()")

def read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary):
    try:
        contents_dict = {}
        current_page = [
            i for i in range(
                page_and_base_url_dictionary["start_page"],
                page_and_base_url_dictionary["last_page"] + 1)]
        
        for index, url in enumerate(get_url_list(page_and_base_url_dictionary)):
            read_a_list_of_posts_and_save_it_to_dictionary(url, contents_dict)
    except:
        print("error on function wlt.dcinside.read_lists_of_posts_and_save_it_to_csv()")

if __name__ == "__main__":
    pass