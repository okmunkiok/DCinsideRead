import time
import random
random.seed(time.time())
import string
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

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
        directories_dictionary = {
            "url_list_path": os.getcwd() + "/data/" + str(community_name) + "/"
        }
        directories_dictionary["temp_raw_data_path"] = directories_dictionary["url_list_path"] + "temp_raw_data/"
        directories_dictionary["merged_data_path"] = directories_dictionary["url_list_path"] + "merged_data/"
        return directories_dictionary
    except:
        print_error(inspect.currentframe())

# def check_and_make_data_directories(community_name):
def check_and_make_data_directories(community_name = "dcinside"):
    try:
        directories_dictionary = get_directories_dictionary(community_name)
        for path in list(directories_dictionary.values()):
            if os.path.exists(path) == False:
                os.makedirs(path)
        return directories_dictionary
    except:
        print_error(inspect.currentframe())

def delete_all_legacy_data(community_name = "dcinside", delete_leagacy_temp_raw_data = False, delete_legacy_merged_data = False, file_header = ""):
    try:
        if delete_leagacy_temp_raw_data == True:
            directories_dictionary = get_directories_dictionary(community_name)
            for path in list(directories_dictionary.values()):
                if path == directories_dictionary["temp_raw_data_path"]:
                    if os.path.exists(path):
                        for file in os.scandir(path):
                            if file_header in file.path:
                                os.remove(file.path)
                    break
        if delete_legacy_merged_data == True:
            directories_dictionary = get_directories_dictionary(community_name)
            for path in list(directories_dictionary.values()):
                if path == directories_dictionary["merged_data_path"]:
                    if os.path.exists(path):
                        for file in os.scandir(path):
                            if file_header in file.path:
                                os.remove(file.path)
                    break
        return
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

def get_tuple_list_from_dictionary_to(column_data_type_dictionary):
    try:
        data_types_tuple_list = []
        for key in column_data_type_dictionary:
            data_types_tuple_list.append((key, column_data_type_dictionary[key]))
        return data_types_tuple_list
    except:
        print_error(inspect.currentframe())

def create_empty_dataframe_with_column_data_types_dictionary(column_data_type_dictionary):
    try:
        temp_ndarray = np.empty(0, dtype = get_tuple_list_from_dictionary_to(column_data_type_dictionary))
        return pd.DataFrame(temp_ndarray)
    except:
        print_error(inspect.currentframe())

if __name__ == "__main__":
    pass