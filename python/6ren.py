import json
import os
from datetime import datetime

import lunar_list

# import fetch

now = datetime.now()


def get_chinese_time(now):
    # 判断当前时间介于哪个时辰
    hour = now.hour
    # 将小时数映射到列表索引上
    index = hour // 2
    # 由于0和23小时映射到相同的索引，需要单独处理23小时的情况
    if hour == 23:
        index = 0
    return lunar_list.time_list[index]


def get_lunar(date):
    year = date[:4]
    date_time = date[5:]
    # 获取当前日期的农历
    filename = f'{year}.json'
    data_folder = os.path.dirname(os.getcwd()) + '\lunar\data'
    with open(f'{data_folder}\{filename}', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data[date_time]
    # return fetch.get_lunar_by_date(date)


def get_result(sum):
    return (sum) % 6


def main():
    current_time = get_chinese_time(now)
    current_time_index = lunar_list.time_list.index(current_time)
    current_date = now.strftime("%Y-%m-%d")
    current_lunar = get_lunar(current_date)
    current_lunar_month = current_lunar['month']
    current_lunar_month_index = lunar_list.month_list.index(
        current_lunar_month)
    current_lunar_day = current_lunar['day']
    current_lunar_day_index = lunar_list.day_list.index(current_lunar_day)

    sum = current_lunar_month_index + current_lunar_day_index + current_time_index
    result = get_result(sum)

    print(
        f'{current_lunar_month}{current_lunar_day} {current_time}')
    print(f'{lunar_list.result_list[result]}')
    print(f'断曰：{lunar_list.gua_ci[result]}。')


if __name__ == "__main__":
    main()
