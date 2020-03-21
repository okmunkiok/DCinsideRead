import DCinsideRead.dcinside as dc
import DCinsideRead.common as common
from selenium import webdriver
from bs4 import BeautifulSoup
import re
# print(page_and_base_url_dictionary)
# print(page_and_base_url_dictionary["last_page"])
# dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary, pre_delete_all_legacy_data_or_not=True)
from functools import partial
from multiprocessing import Pool, freeze_support
import time
import datetime


def test(reply_button_href_list=0):
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    # regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
    # contents = bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)})
    reply_button_tag = bs.find("div", class_="cmt_paging")
    reply_button_list = reply_button_tag.find_all("a")
    # print(reply_button_list)
    reply_button_href_list = []
    for reply_button in reply_button_list:
        if reply_button.text not in ["처음", "이전", "다음", "끝"]:
            reply_button_href_list.append(reply_button.attrs["href"])

    for index, reply_button_href in enumerate(reply_button_href_list):
        whether_next = False
        condition1 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0) and\
                     (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) <= 15)
        condition2 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 14) and\
                     (30 >= int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) > 15)
        condition3 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0) and\
                     (45 >= int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) > 30)
        condition4 = (int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 14) and\
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
        bs = BeautifulSoup(html, "html.parser")
        reply_button_tag = bs.find("div", class_="cmt_paging")
        reply_button_list = reply_button_tag.find_all("a")
        reply_button_href_list = []
        for reply_button in reply_button_list:
            if reply_button.text not in ["처음", "이전", "끝"]:
                reply_button_href_list.append(reply_button.attrs["href"])

        if whether_next:
            driver.find_element_by_xpath("//a[@href=\"" + reply_button_href_list[index + 1] + "\"]").click()
            html = driver.page_source
            bs = BeautifulSoup(html, "html.parser")
            reply_button_tag = bs.find("div", class_="cmt_paging")
            reply_button_list = reply_button_tag.find_all("a")
            reply_button_href_list = []
            for reply_button in reply_button_list:
                if reply_button.text not in ["처음", "이전", "끝"]:
                    reply_button_href_list.append(reply_button.attrs["href"])
            test(reply_button_href_list)

if __name__ == "__main__":
    start_time = time.time()
    page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("클래식")
    # page_and_base_url_dictionary["last_page"] = 500
    page_and_base_url_dictionary["last_page"] = 1
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(options=options)
    # url = "https://gall.dcinside.com/board/view/?id=classic&no=345397&page=1"
    url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=8225358&exception_mode=recommend&page=215"
    # url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=6231119&exception_mode=recommend&page=215"
    # url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=13727444&t=cv&exception_mode=recommend&page=2"
    # url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=13503395&exception_mode=recommend&page=4"
    # url = "https://gall.dcinside.com/board/view/?id=baseball_new8&no=13727444&exception_mode=recommend&page=2"
    # url = "https://gall.dcinside.com/board/view/?id=hit&no=14996&page=14"
    # url = "https://gall.dcinside.com/board/view/?id=event_voicere&no=2229941&exception_mode=recommend&page=1"
    driver.get(url)
    # b = driver.find_element_by_xpath('//*[@id="comment_li_1928327"]/div/div[2]/p')

    test()
    # html = driver.page_source
    # bs = BeautifulSoup(html, "html.parser")
    # # regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
    # # contents = bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)})
    # reply_button_tag = bs.find("div", class_="cmt_paging")
    # reply_button_list = reply_button_tag.find_all("a")
    # # print(reply_button_list)
    # reply_button_href_list = []
    # for reply_button in reply_button_list:
    #     if reply_button.text not in ["처음", "이전", "다음", "끝"]:
    #         reply_button_href_list.append(reply_button.attrs["href"])
    #
    # for index, reply_button_href in enumerate(reply_button_href_list):
    #     whether_next = False
    #     if int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0:
    #         whether_next = True
    #     driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").click()
    #
    #     html = driver.page_source
    #     bs = BeautifulSoup(html, "html.parser")
    #     reply_button_tag = bs.find("div", class_="cmt_paging")
    #     reply_button_list = reply_button_tag.find_all("a")
    #     reply_button_href_list = []
    #     for reply_button in reply_button_list:
    #         if reply_button.text not in ["처음", "이전", "끝"]:
    #             reply_button_href_list.append(reply_button.attrs["href"])
    #
    #     if whether_next:
    #         driver.find_element_by_xpath("//a[@href=\"" + reply_button_href_list[index + 1] + "\"]").click()
    #         html = driver.page_source
    #         bs = BeautifulSoup(html, "html.parser")
    #         reply_button_tag = bs.find("div", class_="cmt_paging")
    #         reply_button_list = reply_button_tag.find_all("a")
    #         reply_button_href_list = []
    #         for reply_button in reply_button_list:
    #             if reply_button.text not in ["처음", "이전", "끝"]:
    #                 reply_button_href_list.append(reply_button.attrs["href"])
    #         print("qwer")
    #         continue
    #
    # print(reply_button_href_list)

            # print(reply_button_list)
            # for reply_button in reply_button_list:
            #     print(reply_button.text == "다음")
            #     if reply_button.text == "다음":
            #         print("asdf")
            #         driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").click()
            #         print("qwer")
                    # break
            # print(reply_button_href_list)
            # continue

    # print(reply_button_href)
    # print(reply_button_href_list)
        # print(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text)
        # print(int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15)
        # print(int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15)
        # if int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0:
        #     print("asdf")
    # print(reply_button_href_list)
        # print("qwer")
        # if int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0:
        #     print("asdf")
        # else:
        #     print("asf")
        #     print(reply_button_href_list)
        # if int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 == 0:
        #     print("asdf")

        # if int(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text) % 15 != 0:
        #     print("asdf")
                # break
            # continue
            # print(reply_button_href)
        # pass
    # print(reply_button_href_list)
    # print(reply_button_href_list)

    # for reply_button in reply_button_list:
    #     if reply_button.attrs["href"] is "javascript:viewComments(15,'D')":
    #         pass

    # print(reply_button_href_list)
    # print(type(reply_button_href_list[0]))
    # print(reply_button_href_list[0])
    # if len(reply_button_href_list) > 1:
    #     print("asdf")

# def get_reply_button_href_list(url)



    # for reply_button_href in reply_button_href_list:
    #     try:
    #         driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]")
    #     except:
    #         # print("asdf")
    #         get_reply_button_next("다음").click()
    #         # reply_button_href_list.append(get_reply_button_next())
    #         reply_button_href_list = get_reply_button_next()
    #         # continue
    #         # break
    #         # driver.find_element_by_xpath("//a[@href=\"" + get_reply_button_next() + "\"]").click()
    #     else:
    #         if driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text not in ["처음", "이전", "끝"]:
    #             driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").click()




# def get_reply_beyond_buttons(driver, *args):
#     html = driver.page_source
#     bs = BeautifulSoup(html, "html.parser")
#     regular_expression_for_getting_reply = r"comment_li_[^0]\w*"
#     contents = bs.find_all("li", {"id": re.compile(regular_expression_for_getting_reply)})
#     reply_button_tag = bs.find("div", class_="cmt_paging")
#     reply_button_list = reply_button_tag.find_all("a")
#     reply_button_href_list = []
#     for reply_button in reply_button_list:
#         reply_button_href_list.append(reply_button.attrs["href"])
#     pass

        # print(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text)
        # if driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text == "다음":
        #     # print(driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").text)
        #     print("asdf")
        #     break
        # else:
        #     driver.find_element_by_xpath("//a[@href=\"" + reply_button_href + "\"]").click()


        
        
    # driver.find_element_by_xpath("//a[")
    # driver.find_element_by_xpath("//a[@href=reply_button_href_list[0]")
    # driver.find_element_by_xpath("//a[@href=", reply_button_href_list[0], "\"")
    # print(reply_button_href_list)
    # print(reply_button)
    # driver.find_element_by_xpath("//a[@href=\"javascript:viewComments(2,\'D\')\"]").click()
    # driver.find_element_by_css_selector("a[href=javascript:viewComments(2,\'D\')]").click()
    # b = driver.find_element_by_class_name("cmt_paging")
    # print(b)
    # contents += contents
    # for content in contents:
    #     if content.find("span", class_="date_time") is not None:
    #         title_tag = content.find("p", class_="usertxt ub-word")
    #         if title_tag is not None:
    #             title = title_tag.text
    #         else:
    #             title = "(보이스 리플)"
    #         print(title)

        # date_tag = content.find("span", class_="date_time")
        # if date_tag is not None:
        #     date = common.replace_several(date_tag.text, [".", ":", " "], "")
        #     if len(date) < 14:
        #         date = str(datetime.date.today().year) + date
        #     # print(len(date))
        # # print(date_tag.text)
        #     print(date)
    # print(contents)
    # print(bs)

    # print(bs.find("li", id="comment_li_1928327"))
    # print(bs.find("div", class_="clear cmt_txtbox btn_reply_write_all"))
    # b = a.find_ele
    # print(b.text)
    # driver.close()
    # post_list_dictionary = {0: {"a": "b"}}
    # time_list = []
    # multi_processes_list = [i for i in range(2, 32 + 1)]
    # for multi_processes in multi_processes_list:
    #     for i in range(3):
    #         start_time = time.time()
    #         dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary,
    #                                                   multi_processes_on=True, multi_processes=multi_processes)
    #         time_list.append(time.time() - start_time)

    # for i in range(len(time_list)):
    #     print("multi ", i + 1, time_list[i])
    #     if i > 0 and i % 3 == 0:
    #         print("\n")

    # dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary,
    #                                           multi_processes_on=True, multi_processes=4)
    # print(post_list_dictionary)
    # print("총 %.2f초 걸렸다" % (time.time() - start_time))
    # dc.get_reply(page_and_base_url_dictionary, multi_processes_on=True)
    # dc.get_reply(page_and_base_url_dictionary, multiprocessing=True)


    # start_time = time.time()
    # freeze_support()
    # pool = Pool(processes=4)
    # pool.map(partial(dc.read_a_list_of_posts_and_save_it_to_dictionary,
    #                  page_and_base_url_dictionary=page_and_base_url_dictionary),
    #          dc.get_url_list(page_and_base_url_dictionary))
    # pool.close()
    # print("multiprocessing에 %.2f초 걸렸다" % (time.time() - start_time))





# for url in dc.get_url_list(page_and_base_url_dictionary):
#     dc.read_a_list_of_posts_and_save_it_to_dictionary(url,
#                                                       page_and_base_url_dictionary=page_and_base_url_dictionary)


# from functools import partial
# from itertools import repeat
# from multiprocessing import Pool, freeze_support
#
#
# def func(a, *args, b, c, d, **kwargs):
#     # d.append(a+b+c)
#     d = a+b+c
#     print(d)
#     # print(a+b+c)
#     return a + b + c
#
#
# def main():
#     a_args = [1,2,3]
#     second_arg = 1
#     third_arg = 2
#     fourth_arg_list = []
#     # with Pool() as pool:
#     #     # L = pool.starmap(func, [(1, 1), (2, 1), (3, 1)])
#     #     # M = pool.starmap(func, zip(a_args, repeat(second_arg)))
#     #     # N = pool.map(partial(func, b=second_arg), a_args)
#     #     # assert L == M == N
#     #     # pool.starmap(func, zip(a_args, repeat(second_arg)))
#     #     pool.map(partial(func, c=third_arg, d=fourth_arg_list, b=second_arg), a_args)
#     #     # print(fourth_arg_list)
#     pool = Pool(processes=2)
#     pool.map(partial(func, c=third_arg, d=fourth_arg_list, b=second_arg), a_args)
#     print(fourth_arg_list)
#
#
# if __name__=="__main__":
#     freeze_support()
#     main()