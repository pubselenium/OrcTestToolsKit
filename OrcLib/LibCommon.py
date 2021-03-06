# coding=utf-8
from importlib import import_module
import time
import re


def is_equal_str(str_a, str_b):
    """
    判断字符串相等，None 作为空串处理
    :param str_a: string，参数 A
    :param str_b: string，参数 B
    :return: bool
    """
    if str_a is None:
        str_a = ""
    if str_b is None:
        str_b = ""

    return str_a == str_b


def is_true(p_str):
    return "TRUE" == p_str


def is_false(p_str):
    return "FALSE" == p_str


def is_null(p_str):
    """
    判断字符串为空，None 作为空串处理
    :param p_str: string 输入参数，字符串
    :return: bool
    """
    return (p_str is None) or\
           ("" == p_str) or\
           ("None" == p_str)


def gen_date_str():
    return time.strftime("%Y%m%d")


class OrcCovert:

    def __init__(self):
        pass

    @staticmethod
    def time2str(p_time):
        try:
            _res = p_time.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            _res = None
        return _res

    @staticmethod
    def str2time(p_str):
        try:
            _res = time.mktime(time.strptime(p_str, "%Y-%m-%d %H:%M:%S"))
        except AttributeError:
            _res = None
        return _res
