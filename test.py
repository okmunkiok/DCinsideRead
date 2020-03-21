import DCinsideRead
import DCinsideRead.dcinside as dc
import pandas as pd
import os

page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("국내야구")
# page_and_base_url_dictionary["url"] = "https://gall.dcinside.com/mgallery/board/lists/?id=lovelyviolin"
# page_and_base_url_dictionary["base_url"] = "https://gall.dcinside.com/mgallery/board/lists/?id=lovelyviolin" + "&page="
# print(page_and_base_url_dictionary)
# print(dc.get_last_page_number(page_and_base_url_dictionary["url"]))
page_and_base_url_dictionary["last_page"] = dc.get_last_page_number(page_and_base_url_dictionary["url"])
print(page_and_base_url_dictionary["last_page"])
# page_and_base_url_dictionary["last_page"] = 367
page_and_base_url_dictionary["save_csv_page_unit"] = 10
# dc.get_url_list(page_and_base_url_dictionary)
# print(dc.get_url_list(page_and_base_url_dictionary))
# print(page_and_base_url_dictionary["last_page"])
dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary)


# for file_name in os.listdir(page_and_base_url_dictionary["merged_data_path"]):
#     if dc.get_csv_header(page_and_base_url_dictionary, read_post_list=True) in file_name:
#         csv_file_name = file_name
#
# print(csv_file_name)
# print(page_and_base_url_dictionary["merged_data_path"] + csv_file_name)
# df = pd.read_csv(page_and_base_url_dictionary["merged_data_path"] + csv_file_name,
#                  index_col=0)
# df = df.sort_values(by=["post_number"], axis=0, ascending=False)
# df = df[df["post_number"] != 0]



# # dc.get_reply(page_and_base_url_dictionary)
# #
# #
# # import multiprocessing
# # import time
# #
# # # 시작시간
# # start_time = time.time()
# #
# #
# # # 멀티쓰레드 사용 하는 경우 (20만 카운트)
# # # Pool 사용해서 함수 실행을 병렬
# # def count(name):
# #     for i in range(1, 100):
# #         print(name, " : ", i)
# #
# #
# # num_list = ['p1', 'p2', 'p3', 'p4']
# #
# # if __name__ == '__main__':
# #     # 멀티 쓰레딩 Pool 사용
# #     pool = multiprocessing.Pool(processes=4)  # 현재 시스템에서 사용 할 프로세스 개수
# #     pool.map(count, num_list)
# #     pool.close()
# #     pool.join()
# #
# # print("--- %s seconds ---" % (time.time() - start_time))
#
# # import multiprocessing
# #
# #
# # def get_reply_all_html(name, *args, dic, **kwargs):
# #     for i in range(3):
# #         print(name)
# #         # print(str(name))
# #         # print("2")
# #         # dic[str(name) + str(i)] = i
# #
# #
# # name_list = ["p1", "p2", "p3", "p4"]
# # pool = multiprocessing.Pool(processes=2)
# # dic = {}
# # # pool.map(get_reply_all_html, name_list, dic)
# # pool.map(get_reply_all_html, name_list)
# # pool.close()
# # pool.join()
# #
# # print(dic)
#
#
# import multiprocessing
# import time
#
# # 시작시간
# start_time = time.time()
#
#
# # 멀티쓰레드 사용 하는 경우 (20만 카운트)
# # Pool 사용해서 함수 실행을 병렬
# def get_reply_all_html(name, *args, dic, **kwargs):
#     for i in range(1, 5):
#         # print(name, " : ", i)
#         print(name)
#
# num_list = ['p1', 'p2', 'p3', 'p4']
#
# if __name__ == '__main__':
#     dic = {}
#     # 멀티 쓰레딩 Pool 사용
#     pool = multiprocessing.Pool(processes=4)  # 현재 시스템에서 사용 할 프로세스 개수
#     # pool.map(get_reply_all_html, num_list)
#     pool.map()
#     pool.close()
#     pool.join()
#
# print("--- %s seconds ---" % (time.time() - start_time))