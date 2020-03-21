from bs4 import BeautifulSoup
import DCinsideRead.common as common
import DCinsideRead.dcinside as dc
import pandas as pd
import time

if __name__ == "__main__":
    # page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("국내야구", "개념글")
    page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("국내야구")
    page_and_base_url_dictionary["last_page"] = 100
    print(page_and_base_url_dictionary["last_page"])
    start_time = time.time()
    # dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary,
    #                                           multiprocessing=True)
    # dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary,
    #                                           multiprocessing=True,
    #                                           processes=8)
    print("총 %.2f초 걸렸다" % (time.time() - start_time))
    csv_file_path_name = "baseball_new8_recommended post list 20200319142455.csv"
    csv = pd.read_csv(csv_file_path_name, index_col=0)
    # merged_dataframe = merged_dataframe.sort_values(by=["post_number"], axis=0, ascending=False)
    csv = csv.sort_values(by=["reply_number"], axis=0, ascending=False)
    # print(type(csv))

# a = [1, 2, 3]
#
# for i in a:
#     if i % 2 == 0:
#         a = []
#     print(a)