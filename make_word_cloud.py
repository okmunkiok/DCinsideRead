import pandas as pd
import DCinsideRead
import DCinsideRead.dcinside as dc
import os
import numpy as np
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# import pygame
# import pytagcloud

page_and_base_url_dictionary = dc.get_page_and_base_url_dictionary("국내야구")
page_and_base_url_dictionary["last_page"] = dc.get_last_page_number(page_and_base_url_dictionary["url"])
# page_and_base_url_dictionary["last_page"] = 100
page_and_base_url_dictionary["save_csv_page_unit"] = 10

for file_name in os.listdir(page_and_base_url_dictionary["merged_data_path"]):
    if dc.get_csv_header(page_and_base_url_dictionary, read_post_list=True) in file_name:
        csv_file_name = file_name
df = pd.read_csv(page_and_base_url_dictionary["merged_data_path"] + csv_file_name,
                 index_col=0)
df = df.sort_values(by=["post_number"], axis=0, ascending=False)
df = df[df["post_number"] != 0]
# df = df[df["date"] < 20141231235959]
# df = df[df["date"] > 20141231235959]
# df = df[df["date"] > 2011231235959]
# df = df[df["date"] > 20141231235959]
# df = df[df["date"] < 20151231235959]
# df = df[df["date"] > 20191231235959]
df = df.reset_index(drop=False, inplace=False)
df_title_str_concat = df["title"].str.cat(sep="\n")
# title_list = df_title_str_concat.split("\n")
okt = Okt()
# morphs = []
nouns = okt.nouns(df_title_str_concat)
# print(morphs)
count = Counter(nouns)
tags = count.most_common(100)

wc = WordCloud(font_path='NanumSquare_acL.ttf', background_color='white', width=9000, height=6000)
# print(dict(tags))
cloud = wc.generate_from_frequencies(dict(tags))
plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
fig = plt.gcf()
plt.show()
fig.savefig("야갤.png", dpi=fig.dpi)

# print(dict(tags))

# for title in title_list:
#     morphs.append(okt.nouns(title))
# print(morphs)
# word_list = []
# # nouns = Okt.nouns(data)
# # noun_adj_adv_list = []
# # for sentence in morphs:
# #     for word, tag in sentence:
# #         # word_list.append(word)
# #         if tag in ['Noun']:
# #         # if tag in ['Noun'] and ("것" not in word) and ("내" not in word)and ("나" not in word)and ("수"not in word) and("게"not in word)and("말"not in word):
# #             noun_adj_adv_list.append(word)
# # print(noun_adj_adv_list)
# # count = Counter(noun_adj_adv_list)
# # count = Counter(word_list)
# # print(count)
# count = Counter(morphs)
# print(count)
# words = dict(count.most_common(100))
#
# str_dic = ""
# for key in words:
#     str_dic += (str(key) + ": " + str(words[key]))
#     str_dic += "\n"
#
# tag2 = count.most_common(100)
# tag_list = pytag
    # print(key, words[key])
# print(str_dic)
# print(words)
# print(words)
# print(len(title_list))
# twitter = Okt()
# morphs = []
# for sentence in title_list:
#     print(sentence)
# for sentence in title_list:
#     morphs.append(twitter.pos(sentence))
# print(morphs)
# morphs.append(twitter.pos(df_title_str_concat))
# print(morphs)
# print(df_title_str_concat[1])
# print(len(df_title_str_concat))
# for i in df_title_str_concat:
#     print(i)
# text_file = open("text_file.txt", "w")
# text_file.write(df_title_str_concat)
# text_file.close()
# print(type(df_title_str_concat))
# f = open(os.getcwd(), 'w')

# x = df["title"]
# df = df[df["date"] > 20200101]
# print()
# df["date"].describe()
