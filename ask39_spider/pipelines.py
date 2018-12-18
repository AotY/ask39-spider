# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from ask39_spider.constant import Constant
from ask39_spider.items import QuestionItem, DoctorItem


class Ask39SpiderPipeline(object):
    def __init__(self):
        mode = 'w'
        self.convos_file = open(Constant.convos_path, mode, encoding='utf-8')
        self.doctor_file = open(Constant.doctor_path, mode, encoding='utf-8')

    def process_item(self, item, spider):
        if item is None:
            return item

        if isinstance(item, QuestionItem):
            logging.info('save question to file.')
            # save to question
            self.convos_file.write('%s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s\n' %
                                   (item['q_id'], item['d_id'], item['title'], item['query'], item['response'],
                                    item['sub'], item['gender'], item['age'], item['onset'], item['labels']))
        else:
            logging.info('save doctor to file.')
            # save to doctor
            self.doctor_file.write('%s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s SPLIT %s\n' %
                                   (item['d_id'], item['d_name'], item['d_job'], item['d_hospital'],
                                    item['d_department'], item['d_excel'], item['d_about']))
        return item

    def __del__(self):
        #  self.convos_file.close()
        #  self.doctor_file.close()
        pass
