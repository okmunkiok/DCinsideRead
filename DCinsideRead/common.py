import random
import string
import os
import requests
import urllib.request
from bs4 import BeautifulSoup

request_iterate_limit = 10


def get_fake_header(*header_length_max):
    try:
        header_length_min = 3
        if len(header_length_max) != 0 and type(header_length_max[0]) == int:
            header_length_max = abs(header_length_max[0]) + header_length_min
        else:
            header_length_max = header_length_min * 2
        header_length = random.randint(header_length_min, header_length_max)
        header = ""
        for i in range(header_length):
            header += random.choice(string.ascii_letters)
        headers = {"User-Agent": header}
        return headers
    except:
        print("error on function wlt.common.get_fake_header()")

def get_directories_dictionary(community_name):
    try:
        directory_info_dictionary = {
            "url_list_path": os.getcwd() + "/data/" + community_name + "/"
        }
        directory_info_dictionary["temp_raw_data_path"] = directory_info_dictionary["url_list_path"] + "temp_raw_data/"
        directory_info_dictionary["merged_data_path"] = directory_info_dictionary["url_list_path"] + "merged_data/"
        return directory_info_dictionary
    except:
        print("error on function wlt.common.get_directories_dictionary()")

def check_and_make_data_directories(community_name):
    try:
        directory_info_dictionary = get_directories_dictionary(community_name)
        for path in list(directory_info_dictionary.values()):
            if os.path.exists(path) == False:
                os.makedirs(path)
        return directory_info_dictionary
    except:
        print("error on function wlt.common.check_and_make_data_directions()")

def delete_all_legacy_raw_data(community_name):
    try:
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
    except:
        print("error on function wlt.common.delete_all_legacy_raw_data()")

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

        # print("requests.get이", request_iterate_limit, "번 거절되었으므로 header를 바꿔 다시 시도합니다")
        for request_iterate in range(request_iterate_limit):
            try:
                get_requests = requests.get(url, headers = get_fake_header(random.randint(10, 20)))
            except:
                continue
            else:
                request_iterate = 0
                return get_requests
        print("header를 바꿔 다시", request_iterate_limit, "번 시도하여도 거절되어서 None을 반환하고 종료합니다")
        return None
    except:
        print("error on function wlt.common.requests_get()")
    
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

        # print("urllib.request.Request가", request_iterate_limit, "번 거절되었으므로 header를 바꿔 다시 시도합니다")
        for request_iterate in range(request_iterate_limit):
            try:
                get_Request = urllib.request.Request(url, headers = get_fake_header(random.randint(10, 20)))
            except:
                continue
            else:
                request_iterate = 0
                return get_Request
        print("header를 바꿔 다시", request_iterate_limit, "번 시도하여도 거절되어서 None을 반환하고 종료합니다")
        return None
    except:
        print("error on function wlt.common.urllib_request_Request()")

if __name__ == "__main__":
    pass