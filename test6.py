import DCinsideRead.dcinside as dc
import time

if __name__ == "__main__":
    start_time = time.time()
    page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("클래식", "개념글")
    page_and_base_url_dictionary["last_page"] = 1
    print("start_page =", page_and_base_url_dictionary["start_page"])
    print("last_page =", page_and_base_url_dictionary["last_page"])
    dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary, multiprocessing=True)
    print("총 %.2f초 걸렸다" % (time.time() - start_time))