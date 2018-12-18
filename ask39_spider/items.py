# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class QuestionItem(scrapy.Item):
    # query
    q_id = Field()  # question id

    d_id = Field()  # doctor id

    sub = Field() # 

    title = Field()  # title
    gender = Field()  # gender
    age = Field()  # age
    onset = Field()  # time of onset

    labels = Field()  # labels

    query = Field()  # query

    response = Field()  # including zw


class DoctorItem(scrapy.Item):
    # doctor
    d_id = Field()  # doctor id
    d_name = Field()  # doctor name
    d_job = Field()  # doctor job
    d_hospital = Field()  # hospital of doctor
    d_department = Field()  # department of doctor
    d_excel = Field()  # good at
    d_about = Field()  # about


class Ask39SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
