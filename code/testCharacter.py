#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Tianyanfei
# @Mail    : tyfdream@163.com
# @Data    : 2016-11-24 16:17:48
# @Version : python 2.7

import os

# 判断一个unicode是否是汉字
def is_chinese(uchar):         
    if u'\u4e00' <= uchar<=u'\u9fff':
        return True
    else:
        return False

# 判断一个unicode是否是数字
def is_number(uchar):
    if u'\u0030' <= uchar and uchar<=u'\u0039':
        return True
    else:
        return False

# 判断一个unicode是否是英文字母
def is_alphabet(uchar):         
    if (u'\u0041' <= uchar<=u'\u005a') or (u'\u0061' <= uchar<=u'\u007a'):
        return True
    else:
        return False

# 判断是否非汉字，数字和英文字符 adapt to multi-characters
def is_other(uchar):
    if len(uchar) > 1: return True
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return False
    else:
        return True

if __name__=="__main__":
    ustring=u'中国 a d111*'
    # 判断是否有其他字符；
    print is_other(u'*')
    for item in ustring:
    	print item
        if is_chinese(item): 
        	print 'chinese'
        elif is_alphabet(item):
        	print 'alphabet'
        elif is_number(item):
        	print 'digital'
        elif is_other(item):
        	print 'other'