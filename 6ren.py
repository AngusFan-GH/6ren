import json
from datetime import datetime

# 六壬数组
result_array = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']
time_array = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时',
              '午时', '未时', '申时', '酉时', '戌时', '亥时']
month_array = ['一月', '二月', '三月', '四月', '五月', '六月',
               '七月', '八月', '九月', '十月', '十一月', '十二月']
day_array = ['初一', '初二', '初三', '初四', '初五', '初六',
             '初七', '初八', '初九', '初十', '十一', '十二',
             '十三', '十四', '十五', '十六', '十七', '十八',
             '十九', '二十', '廿一', '廿二', '廿三', '廿四',
             '廿五', '廿六', '廿七', '廿八', '廿九', '三十']

guaci_array = [
    '大安事事昌，求财在坤方，失物去不远，宅舍保安康。行人身未动，病者主无妨，将军回田野，仔细兴推祥',
    '留连事难成，求谋月未明，凡事只宜缓，去者未回程；失物南方见，急讨方称心，更须防口舌，人口且太平',
    '速喜喜来临，求财向南行，失物申未午，逢人路上寻；官事有福德，病者无祸侵，田宅六畜吉，行人有喜音',
    '赤口主口舌，官非切要防，失物急去寻，行人有惊慌。六畜多惊怪，病者出西方，更须防诅咒，恐怕染瘟疫',
    '小吉最吉昌，路上好商量，阴人来报喜，失物在坤方；行人立便至，交易甚是强，凡是皆和合，病者辱上苍',
    '空亡事不祥，阴人多乖张，求财无利益，行人有灾秧；失物寻不见，官事有刑伤，病人逢暗鬼，禳解保安康',
]

now = datetime.now()

# 判断当前时间介于哪个时辰


def get_chinese_time(now):
    if now.hour >= 23 or now.hour < 1:
        return '子时'
    elif now.hour >= 1 and now.hour < 3:
        return '丑时'
    elif now.hour >= 3 and now.hour < 5:
        return '寅时'
    elif now.hour >= 5 and now.hour < 7:
        return '卯时'
    elif now.hour >= 7 and now.hour < 9:
        return '辰时'
    elif now.hour >= 9 and now.hour < 11:
        return '巳时'
    elif now.hour >= 11 and now.hour < 13:
        return '午时'
    elif now.hour >= 13 and now.hour < 15:
        return '未时'
    elif now.hour >= 15 and now.hour < 17:
        return '申时'
    elif now.hour >= 17 and now.hour < 19:
        return '酉时'
    elif now.hour >= 19 and now.hour < 21:
        return '戌时'
    elif now.hour >= 21 and now.hour < 23:
        return '亥时'


# 获取当前日期的农历


def get_lunar(date):
    filename = '1901-2100_lunar.json'
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data[date]['lunar']


def get_result(sum):
    return (sum - 2) % 6


current_time = get_chinese_time(now)
current_time_index = time_array.index(current_time)

current_date = now.strftime("%Y-%m-%d")
current_lunar = get_lunar(current_date)
current_lunar_month_index = month_array.index(current_lunar[:-2])
current_lunar_day_index = day_array.index(current_lunar[-2:])

sum = current_lunar_month_index + current_lunar_day_index + current_time_index

result = get_result(sum)

print(f'{current_lunar} {current_time} {result_array[result]}')
print(f'断曰：{guaci_array[result]}.')
