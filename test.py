import DCinsideRead
import DCinsideRead.dcinside as dc

page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("클래식")
page_and_base_url_dictionary["last_page"] = dc.get_last_page_number(page_and_base_url_dictionary["url"])
page_and_base_url_dictionary["last_page"] = 10
page_and_base_url_dictionary["save_csv_page_unit"] = 6
dc.read_lists_of_posts_and_save_it_to_csv(page_and_base_url_dictionary)


