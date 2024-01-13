import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import chardet
import requests


def convert_date(date_str):
    # 解析日期
    dt = datetime.strptime(date_str, "%Y年%m月%d日")
    # 格式化日期
    formatted_date = dt.strftime("%m-%d")
    return formatted_date


def fetch_lunar_by_year(year):
    url = 'https://www.hko.gov.hk/tc/gts/time/calendar/text/files/T%sc.txt' % year
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.encoding = chardet.detect(response.content)['encoding']
    print(f'Fetching {year} : {response.status_code}!')
    return {
        'data': response.text,
        'year': year
    }


def concat_responses(years):
    with ThreadPoolExecutor(max_workers=len(years)) as executor:
        # 使用map来保持结果的顺序
        responses = executor.map(fetch_lunar_by_year, years)
        return responses


def handle_response(response, month, gan_zhi, chinese_zodiac_sign):
    data = {}
    # 按行读取相应内容
    lines = response.split('\n')
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if '公曆與農曆日期對照表' in line:
            match = re.search(r'\((.*?)\)', line).group(1).split('-')
            gan_zhi = match[0]
            chinese_zodiac_sign = match[1][-1]
        if not re.match(r'^\d{4}年\d{1,2}月\d{1,2}日', line):
            continue
        line_data = line.split()
        date = line_data[0] if line_data else None
        lunar = line_data[1] if len(line_data) > 1 else None
        if '月' in lunar:
            month = lunar
            lunar = lunar + '初一'
        else:
            lunar = month + lunar
        week = line_data[2] if len(line_data) > 2 else None
        solar_term = line_data[3] if len(line_data) > 3 else None
        data[convert_date(date)] = {
            'gan_zhi': gan_zhi,
            'chinese_zodiac_sign': chinese_zodiac_sign,
            'month': lunar[:-2],
            'day': lunar[-2:],
            'week': week
        }
        if solar_term != None:
            data[convert_date(date)]['solar_term'] = solar_term
    return {
        'data': data,
        'month': month,
        'gan_zhi': gan_zhi,
        'chinese_zodiac_sign': chinese_zodiac_sign
    }


def write_file(data, path):
    # 删除已存在的文件
    if os.path.exists(path):
        os.remove(path)

    # 创建新文件并写入数据
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'Write file done: {path}!')


def handle_responses(responses, path):
    month = ''
    gan_zhi = ''
    chinese_zodiac_sign = ''
    # 遍历所有响应，处理数据
    for response in responses:
        year = response['year']
        data = response['data']
        handled_data = handle_response(
            data, month, gan_zhi, chinese_zodiac_sign)
        month = handled_data['month']
        gan_zhi = handled_data['gan_zhi']
        chinese_zodiac_sign = handled_data['chinese_zodiac_sign']
        print(f'Handle data done: {year}!')
        write_file(handled_data['data'], f'{path}\{year}.json')


def main():
    years = list(range(1901, 2101))
    responses = concat_responses(years)
    data_folder = os.path.dirname(os.getcwd()) + '\data'
    handle_responses(responses, data_folder)


if __name__ == '__main__':
    main()
