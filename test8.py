import DCinsideRead.dcinside as dc

if __name__ == "__main__":
    page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("국내야구", "개념글")
    page_and_base_url_dictionary["last_page"] = 1
    print(page_and_base_url_dictionary["last_page"])
    dc.get_reply(page_and_base_url_dictionary, multiprocessing=True)