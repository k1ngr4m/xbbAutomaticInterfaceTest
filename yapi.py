import json
import os.path

import requests as requests


class Yapi:
    def __init__(self):
        self.url = 'http://yapi.xbongbong.com'
        self.token = '132a896d2dc4420896f4cdd3a982bfe77816c6aaacd7252300567ec30a3d38a3'  # 项目token（记得改）
        # self.token = 'db2c30e56df248c641d5e45428a583ab9dc8bf73e9aeefcef3b8effbef7b8007'

    # 获取菜单列表
    def get_cat_menu(self):
        url = self.url + '/api/interface/getCatMenu'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'project_id': 635,  # 项目id
            'token': self.token
        }
        try:
            response = requests.get(url=url, params=body, headers=headers).json()
            # print(response)
            errcode = response['errcode']
            # 成功获取data
            if errcode == 0:
                data = response['data']
                # print(data)
                for i in range(len(data)):
                    cat_id = data[i]['_id']
                    name = data[i]['name']
                    uid = data[i]['uid']
                    # 打印项目信息
                    print(f'cat_id:{cat_id}\tuid:{uid}\t\tname:{name}')
            # 返回数据错误
            else:
                print(errcode)
        except Exception as e:
            print(e)

    # 获取某个分类下接口列表
    def get_interface_list_cat(self, catid):
        url = self.url + '/api/interface/list_cat'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'catid': catid,  # 分组id
            'token': self.token,
            'page': 1,
            'limit': 50
        }
        try:
            file_name = r'data/interface_list_cat.json'
            if not os.path.exists(file_name):
                with open(file_name, 'a', encoding='utf-8') as file:
                    file.close()
            else:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.truncate(0)
            interface_list_cat = []
            response = requests.get(url=url, params=body, headers=headers).json()
            # print(response)
            errcode = response['errcode']
            # 成功获取data
            if errcode == 0:
                data = response['data']
                data_list = data['list']
                # print(data_list)
                for i in range(len(data_list)):
                    interface_id = data_list[i]['_id']
                    title = data_list[i]['title']
                    # 打印接口信息
                    print(f'interface_id:{interface_id}\ttitle:{title}')
                    interface_data_dict = {
                        'interface_id': interface_id,
                        'title': title
                    }
                    interface_list_cat.append(interface_data_dict)
                with open(file_name, 'w', encoding='utf-8') as w_f:
                    result = json.dumps(interface_list_cat, ensure_ascii=False)
                    w_f.write(result)
            # 返回数据错误
            else:
                print(errcode)
        except Exception as e:
            print(e)

    # 获取接口数据（有详细接口数据定义文档）并写入api_data.txt
    def get_interface_detail(self):
        interface_list_cat_filename = r'data/interface_list_cat.json'
        api_data_filename = r'data/api_data.txt'
        if not os.path.exists(api_data_filename):
            with open(api_data_filename, 'a', encoding='utf-8') as file:
                file.close()
        else:
            with open(api_data_filename, 'w', encoding='utf-8') as file:
                file.truncate(0)
        with open(interface_list_cat_filename, 'r', encoding='utf-8') as file:
            interface_list_cat_list = json.load(file)
        for i in range(len(interface_list_cat_list)):
            interface_id = interface_list_cat_list[i]['interface_id']
            url = self.url + '/api/interface/get'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            body = {
                'id': interface_id,  # 接口id
                'token': self.token
            }
            try:
                response = requests.get(url=url, params=body, headers=headers).json()
                print(response)
                errcode = response['errcode']
                # 成功获取data
                if errcode == 0:
                    data = response['data']
                    method = data['method']
                    title = data['title']
                    path = data['path']
                    req_body_other = data['req_body_other']
                    res_body = data['res_body']
                    api_data_dict = {
                        'id': i + 1,
                        'name': title,
                        'url': path,
                        "frontDev": 1,
                        "param": req_body_other
                    }
                    api_data_dict = (str(api_data_dict) + '\r').replace(r'\n', '').replace(' ', '')
                    print(api_data_dict)
                    with open(api_data_filename, 'a+', encoding='utf-8') as w_f:
                        w_f.write(api_data_dict)
                # 返回数据错误
                else:
                    print(errcode)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    yapi = Yapi()
    yapi.get_cat_menu()
    yapi.get_interface_list_cat(1379)
    yapi.get_interface_detail()
