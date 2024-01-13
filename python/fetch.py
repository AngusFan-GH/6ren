import base64

import requests


def get_lunar_by_date(date, logger=False):
    year = date[:4]
    date_time = date[5:]
    # 设置仓库的用户和名称
    username = 'AngusFan-GH'
    repo = '6ren'
    path_to_file = f'lunar/data/{year}.json'

    # 构建API URL
    url = f'https://api.github.com/repos/{username}/{repo}/contents/{path_to_file}'
    if logger:
        print(f'Fetch {year} data from: {url}!')

    # 发起GET请求
    response = requests.get(url)

    # 检查响应状态并处理数据
    if response.status_code == 200:
        raw_data = response.json()
        # 解码base64数据
        data = base64.b64decode(raw_data['content'])
        # 处理编码问题
        data = data.decode('utf-8')
        # 转换为字典
        data = eval(data)
        if logger:
            print(f'Fetch {year} data success!')
        return data[date_time]
    else:
        print(f'Failed to retrieve data: {response.status_code}')
