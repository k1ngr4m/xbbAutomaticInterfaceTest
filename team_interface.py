# coding=utf-8
import json
import os.path

import demjson3 as demjson
import requests
import re
import hashlib
import time
import random
from faker import Faker
import datetime

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
production_token = '3fc702f4c54dc400182dfa8c4c9b67ed1f67cb7609120ad0e888e95691695225'


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

current_time = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
auto_case = r"data/auto_case.txt"
test_report = fr'data/{current_time}_test_report.txt'

if not os.path.exists(test_report):
    with open(test_report, 'a', encoding='utf-8') as file:
        file.close()
else:
    with open(test_report, 'w', encoding='utf-8') as file:
        file.truncate(0)
with open(auto_case, mode='r+', encoding='utf-8') as case_file:
    i = 1
    for line in case_file:
        random_time = random.randint(1, 5)
        time.sleep(random_time)
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
            print(f"第{i}条\t用例名称: ", case_name, "请求地址: ", request_url)
            print("请求报文: ", case_data['request_param'])
            print("用例名称: ", case_name, "实际结果: ", actual_result.text, "\n")
        else:
            if '服务器' in str(actual_result.json()['msg']) or '网络' in str(actual_result.json()['msg']):
                print(f"第{i}条\t用例名称: ", case_name, "请求地址: ", request_url)
                print("请求报文: ", case_data['request_param'])
                print("用例名称: ", case_name, "实际结果: ", actual_result.text, "\n")
                with open(test_report, 'a+', encoding='utf-8') as file:
                    file.write(f"第{i}条\t用例名称: {case_name}, 请求地址:  {request_url}\t")
                    file.write(f"请求报文: {case_data['request_param']}\t")
                    file.write(f"用例名称: {case_name}, 实际结果: {actual_result.text}\n")
            else:
                print(f"第{i}条\t用例名称: ", case_name, "实际结果: ", actual_result.json()['msg'], "\n")
                with open(test_report, 'a+', encoding='utf-8') as file:
                    file.write(f"第{i}条\t用例名称: {case_name}, 实际结果: {actual_result.json()['msg']}\n")
        i = i + 1
