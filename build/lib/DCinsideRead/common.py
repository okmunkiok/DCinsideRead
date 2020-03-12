import time
import random
random.seed(time.time())
import string
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import re

request_iterate_limit = 1000

def print_error(inspect_currentframe):
    print("unexpected error")
    print(inspect_currentframe)
    return

def get_bs_html_parsed(url):
    try:
        req = urllib_request_Request(url)
        html = urllib.request.urlopen(req)
        bs = BeautifulSoup(html, "html.parser")
        return bs
    except:
        print_error(inspect.currentframe())

def get_fake_header(header_length_max = 10):
    try:
        header_length_min = 3
        if header_length_max <= 0 or type(header_length_max != int):
            header_length_max = header_length_min * 5
        header_length = random.randint(header_length_min, header_length_max)
        header = ""
        for i in range(header_length):
            header += random.choice(string.ascii_letters)
        headers = {"User-Agent": header}
        return headers
    except:
        print_error(inspect.currentframe())

# def get_directories_dictionary(community_name):
def get_directories_dictionary(community_name = "dcinside"):
    try:
        directory_info_dictionary = {
            "url_list_path": os.getcwd() + "/data/" + community_name + "/"
        }
        directory_info_dictionary["temp_raw_data_path"] = directory_info_dictionary["url_list_path"] + "temp_raw_data/"
        directory_info_dictionary["merged_data_path"] = directory_info_dictionary["url_list_path"] + "merged_data/"
        return directory_info_dictionary
    except:
        print_error(inspect.currentframe())

# def check_and_make_data_directories(community_name):
def check_and_make_data_directories(community_name = "dcinside"):
    try:
        directory_info_dictionary = get_directories_dictionary(community_name)
        for path in list(directory_info_dictionary.values()):
            if os.path.exists(path) == False:
                os.makedirs(path)
        return directory_info_dictionary
    except:
        print_error(inspect.currentframe())

def delete_all_legacy_data(community_name = "dcinside", delete_raw_data = True, delete_merged_data = False):
    try:
        if delete_raw_data == True:
            directory_info_dictionary = get_directories_dictionary(community_name)
            for path in list(directory_info_dictionary.values()):
                if path == directory_info_dictionary["temp_raw_data_path"]:
                    if os.path.exists(path):
                        for file in os.scandir(path):
                            try:
                                os.remove(file.path)
                            except:
                                continue
                    break

        if delete_merged_data == True:
            directory_info_dictionary = get_directories_dictionary(community_name)
            for path in list(directory_info_dictionary.values()):
                if path == directory_info_dictionary["merged_data_path"]:
                    if os.path.exists(path):
                        for file in os.scandir(path):
                            try:
                                os.remove(file.path)
                            except:
                                continue
                    break
    except:
        print_error(inspect.currentframe())

def requests_get(url):
    try:
        request_iterate = 0
        for request_iterate in range(request_iterate_limit):
            try:
                get_requests = requests.get(url, headers = get_fake_header())
            except:
                continue
            else:
                request_iterate = 0
                return get_requests
        print("header를 매 번 바꾸며 requests.get을", request_iterate_limit, "번 시도하여도 거절되어서 None을 반환하고 종료합니다")
        return None
    except:
        print_error(inspect.currentframe())
    
def urllib_request_Request(url):
    try:
        request_iterate = 0
        for request_iterate in range(request_iterate_limit):
            try:
                get_Request = urllib.request.Request(url, headers = get_fake_header())
            except:
                continue
            else:
                request_iterate = 0
                return get_Request
        print("header를 매 번 바꾸며 urllib.request.Request을", request_iterate_limit, "번 시도하여도 거절되어서 None을 반환하고 종료합니다")
        return None
    except:
        print_error(inspect.currentframe())

def get_match_list_by_regular_expression(regular_expression, from_where):
    try:
        pattern = re.compile(regular_expression)
        return re.findall(pattern, from_where)
    except:
        print_error(inspect.currentframe())

def replace_several(text, to_be_replaced_list, substitute):
    try:
        for to_be_replaced in to_be_replaced_list:
            text = text.replace(to_be_replaced, substitute)
        return text
    except:
        print_error(inspect.currentframe())

if __name__ == "__main__":
    pass