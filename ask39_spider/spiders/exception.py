#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2018 LeonTao
#
# Distributed under terms of the MIT license.

"""
ParseNotSupportedError
"""

class ParseNotSupportedError(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return 'url {} is could not be parsed '.format(self.url)

