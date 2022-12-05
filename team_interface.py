# coding=utf-8
import json

import demjson as demjson
import requests
import re
import hashlib
import time
import random
from faker import Faker

fake = Faker(locale='zh_CN')

# 测试5域名
production_host = 'https://saetestwebf.xbongbong.com.cn'

# 每次请求发送时均会校验sign值
web_headers = {'Host': 'saetestwebf.xbongbong.com.cn',
                    'Accept': 'application/json, text/plain, */*',
                    'Origin': 'https://saetestwebf.xbongbong.com.cn',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                    'sign': '',
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Referer': 'https://saetestwebf.xbongbong.com.cn/',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive'}


# token
production_token = '065873e99c12b4dc832124d3c89db2964c4e573427441f6af8074ac480d3ecd0'



# 生成请求头里的sign值
def create_sign_code(request_parameters, production_token):
    request_parameters = json.dumps(request_parameters)
    parameters = request_parameters + str(production_token)
    sign = hashlib.sha256(parameters.encode('utf-8')).hexdigest()
    return sign


# # 替换请求报文中的部分数据
# def process_request_data(init_data, expected_to_be_replace, need_replace_to_data):
#     page_pattern = re.compile(expected_to_be_replace)
#     matchers = page_pattern.findall(str(init_data))
#     for matcher in matchers:
#         init_data = str(init_data).replace(str(matcher), str(need_replace_to_data))
#     return init_data


auto_case = "/Users/lnwu/Downloads/xbbAutomaticInterfaceTest/auto_case.txt"
with open(auto_case, mode='r+', encoding='utf-8') as case_file:
    for line in case_file:
        time.sleep(5)
        case_data = demjson.decode(line)
        case_name = case_data['case_name']
        request_url = case_data['request_url']
        request_param = case_data['request_param']
        # replace_customer_name = process_request_data(str(case_data['request_param']), "名称", str(fake.address()))
        # request_params = process_request_data(replace_customer_name, "编号", str(fake.address()))
        sign_code = create_sign_code(request_param, production_token)
        web_headers['sign'] = sign_code
        actual_result = requests.post(url=production_host + request_url, json=request_param, headers=web_headers)

        if actual_result.status_code != 200:
            print("用例名称: ", case_name, "请求地址: ", request_url)
            print("请求报文: ", case_data['request_param'])
            print("用例名称: ", case_name, "实际结果: ", actual_result.text, "\n")
        else:
            if '服务器' in str(actual_result.json()['msg']) or '网络' in str(actual_result.json()['msg']):
                print("用例名称: ", case_name, "请求地址: ", request_url)
                print("请求报文: ", case_data['request_param'])
                print("用例名称: ", case_name, "实际结果: ", actual_result.text, "\n")
            else:
                print("用例名称: ", case_name, "实际结果: ", actual_result.json()['msg'], "\n")
