# -*- coding: utf-8 -*
import logging

import scrapy
from ask39_spider.items import QuestionItem, DoctorItem
from ask39_spider.constant import Constant

logger = logging.getLogger('ask39')


class Ask39Spider(scrapy.Spider):
    name = 'ask39'
    allowed_domains = ['ask.39.net', '39.net']
    #  start_urls = ['http://ask.39.net/']

    rotete_user_agent = True

    def __init__(self):
        self.question_template = 'http://ask.39.net/question/%s.html'
        self.doctor_template = 'http://my.39.net/%s'

        self.start_page = 3840295
        #  self.end_page = 70000000
        self.end_page = 56967315

        """
        self.doctor_set = set()
        """

    def start_requests(self):
        #  for cur_page in range(self.start_page, self.end_page):
        for cur_page in range(self.end_page, self.start_page, -1):
            url = self.question_template % cur_page
            logger.info('---> url: %s' % url)
            yield scrapy.Request(url=url, callback=self.parse_question)

        """
        #  self.doctor_set.add('P4349188')
        for doctor in self.doctor_set:
            url = self.doctor_template % doctor
            logger.info('---> url: %s' % url)
            yield scrapy.Request(url=url, callback=self.parse_doctor)
        """

    def parse_question(self, response):
        status = response.status
        url = response.url

        if status != 200:
            logger.info('-------> url: %s, status: %d' % (url, status))
            return None

        # is has reply (selected)
        selected = response.xpath('//*[@class="selected"]')
        if selected is None or len(selected) == 0:
            return None

        selected_img = response.xpath(
            '//*[@class="selected"]/p[@class="sele_img"]/text()')
        if selected_img is None or len(selected_img) == 0:
            return None

        response_count = int(selected_img.extract_first().split('(')[1][:-1])
        if response_count == 0:
            return None

        #  logger.info('response count: %d' % response_count)
        q_id = url.split('/')[-1].split('.')[0]

        #  logger.info('question id: %s' % q_id)

        sub1 = response.xpath('//*[@id="sub"]/span[2]/a[1]/text()').extract_first()
        if sub1 is None:
            sub1 = ''
        sub2 = response.xpath('//*[@id="sub"]/span[3]/a[1]/text()').extract_first()
        if sub2 is None:
            sub2 = ''
        sub3 = response.xpath('//*[@id="sub"]/span[4]/a[1]/text()').extract_first()
        if sub3 is None:
            sub3 = ''
        #  logger.info('sub1: %s sub2: %s' % (sub1, sub2))
        sub = sub1 + '_' + sub2 + '_' + sub3

        title = response.xpath(
            '//*[@class="ask_cont"]/p[@class="ask_tit"]/text()').extract_first()
        if title is None:
            title = ''
        else:
            title = title.replace('\n', '').replace(' ', '')

        gender = response.xpath(
            '//*[@class="ask_cont"]/p[@class="mation"]/span[1]/text()').extract_first()
        if gender is None:
            gender = ''

        age = response.xpath(
            '//*[@class="ask_cont"]/p[@class="mation"]/span[2]/text()').extract_first()
        if age is None:
            age = ''
        else:
            age = age.replace('\n', '').replace(' ', '')[:-1]

        onset = response.xpath(
            '//*[@class="ask_cont"]/p[@class="mation"]/span[3]/text()').extract_first()
        if onset is None:
            onset = ''
        else:
            onset = onset.replace('\n', '').replace(' ', '')

        #  query_text = response.xpath(
            #  '//*[@class="ask_hid"]/p[@class="txt_ms"][1]/text()').extract_first()
        query_texts = response.xpath('//*[@class="ask_hid"]/p[1]//text()').extract()

        if query_texts is None and len(query_texts) == 0:
            return None

        query_text = ''.join(query_texts)
        query_text = query_text.replace(
            '\n', '').replace('\t', '').replace(' ', '')
        if len(query_text) > Constant.q_max_len or len(query_text) < Constant.min_len:
            return None

        labels = []
        label_spans = response.xpath(
            '//*[@class="ask_cont"]/p[@class="txt_label"]/span')
        if label_spans is None or len(label_spans) == 0:
            labels = ''
        else:
            for label_span in label_spans:
                label = label_span.xpath('a/text()').extract_first()
                labels.append(label)

            labels = ','.join(labels)
        #  logger.info('labels: %s' % labels)

        response_divs = response.xpath('//div[@class="selected"]/div')
        if len(response_divs) != response_count:
            return None

        for response_div in response_divs:
            d_url = response_div.xpath(
                'div[@class="doctor_all"]/div[@class="doc_img"]/a/@href').extract_first()
            d_id = d_url.split('/')[-1]

            """
            if d_id not in self.doctor_set:
                self.doctor_set.add(d_id)
            """

            # response text
            response_texts = response_div.xpath(
                'p[@class="sele_txt"]//text()').extract()

            if response_texts is None and len(response_texts) == 0:
                yield None
                continue

            response_text = ''.join(response_texts)

            response_text = response_text.replace(
                '\n', '').replace('\t', '').replace(' ', '')

            if len(response_text) > Constant.r_max_len or len(response_text) < Constant.min_len:
                yield None
                continue

            question_item = QuestionItem()
            question_item['q_id'] = q_id
            question_item['d_id'] = d_id
            question_item['sub'] = sub
            question_item['title'] = title
            question_item['gender'] = gender
            question_item['age'] = age
            question_item['onset'] = onset
            question_item['labels'] = labels
            question_item['query'] = query_text
            question_item['response'] = response_text

            yield question_item

            # contains zw
            zw_divs = response_div.xpath(
                'div[@class="doc_t_strip"]/div[@class="doc_zwenall"]/div[@class="doc_zw"]')
            if zw_divs is None or len(zw_divs) == 0:
                continue
            zw_list = []
            for zw_div in zw_divs:
                zw_text = zw_div.xpath('span/text()').extract()[1]
                zw_text = zw_text.replace('\n', '').replace(
                    '\t', '').replace(' ', '')
                if len(zw_text) > Constant.q_max_len:
                    continue
                zw_list.append(zw_text)
            if len(zw_list) == 0:
                continue
            response_text = ' EOS '.join(zw_list)
            question_item['response'] = response_text

            yield question_item

    def parse_doctor(self, response):
        status = response.status
        d_url = response.url

        if status != 200:
            logger.info('-------> url: %s, status: %d' % (d_url, status))
            return None

        d_id = d_url.split('/')[-1]

        spans = response.xpath('//*[@class="doctor-msg-content"]/div[@class="doctor-msg-person"]/span')
        if spans is None or len(spans) < 2:
            return None

        d_name = spans[0].xpath('text()').extract_first()
        d_job = spans[1].xpath('text()').extract_first()
        d_job = d_job.replace('\xa0', '').replace(' ', '')

        spans = response.xpath(
            '//*[@class="doctor-msg-content"]/div[@class="doctor-msg-job"]/span')
        if spans is None or len(spans) < 2:
            return None
        d_hospital = spans[0].xpath('text()').extract_first()
        d_department = spans[1].xpath('text()').extract_first()

        divs = response.xpath(
            '//*[@class="doctor-msg-content"]/div[contains(@class, "item-article")]')
        if divs is None or len(divs) < 2:
            return None
        d_excel = divs[0].xpath('span[2]/text()').extract_first()
        d_about = divs[1].xpath('span[2]/text()').extract_first()

        doctor_item = DoctorItem()
        doctor_item['d_id'] = d_id
        doctor_item['d_name'] = d_name
        doctor_item['d_job'] = d_job
        doctor_item['d_hospital'] = d_hospital
        doctor_item['d_department'] = d_department
        doctor_item['d_excel'] = d_excel
        doctor_item['d_about'] = d_about

        yield doctor_item
