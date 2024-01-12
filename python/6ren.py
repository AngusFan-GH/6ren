import json
import os
from datetime import datetime

# 六壬数组
result_list = ['大安', '留连', '速喜', '赤口', '小吉', '空亡']

time_list = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时',
             '午时', '未时', '申时', '酉时', '戌时', '亥时']

month_list = ['一月', '二月', '三月', '四月', '五月', '六月',
              '七月', '八月', '九月', '十月', '十一月', '十二月']

day_list = ['初一', '初二', '初三', '初四', '初五', '初六',
            '初七', '初八', '初九', '初十', '十一', '十二',
            '十三', '十四', '十五', '十六', '十七', '十八',
            '十九', '二十', '廿一', '廿二', '廿三', '廿四',
            '廿五', '廿六', '廿七', '廿八', '廿九', '三十']

gua_ci = [
    '大安事事昌，求财在坤方，失物去不远，宅舍保安康。行人身未动，病者主无妨，将军回田野，仔细兴推祥',
    '留连事难成，求谋月未明，凡事只宜缓，去者未回程；失物南方见，急讨方称心，更须防口舌，人口且太平',
    '速喜喜来临，求财向南行，失物申未午，逢人路上寻；官事有福德，病者无祸侵，田宅六畜吉，行人有喜音',
    '赤口主口舌，官非切要防，失物急去寻，行人有惊慌。六畜多惊怪，病者出西方，更须防诅咒，恐怕染瘟疫',
    '小吉最吉昌，路上好商量，阴人来报喜，失物在坤方；行人立便至，交易甚是强，凡是皆和合，病者辱上苍',
    '空亡事不祥，阴人多乖张，求财无利益，行人有灾秧；失物寻不见，官事有刑伤，病人逢暗鬼，禳解保安康',
]

# 天干
tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 生成六十干支列表
gan_zhi = [g + d for g in tian_gan for d in di_zhi]

# 生肖
sheng_xiao = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

now = datetime.now()


def get_chinese_time(now):
    # 判断当前时间介于哪个时辰
    hour = now.hour
    if hour == 23 or hour == 0:
        return time_list[0]
    elif hour == 1 or hour == 2:
        return time_list[1]
    elif hour == 3 or hour == 4:
        return time_list[2]
    elif hour == 5 or hour == 6:
        return time_list[3]
    elif hour == 7 or hour == 8:
        return time_list[4]
    elif hour == 9 or hour == 10:
        return time_list[5]
    elif hour == 11 or hour == 12:
        return time_list[6]
    elif hour == 13 or hour == 14:
        return time_list[7]
    elif hour == 15 or hour == 16:
        return time_list[8]
    elif hour == 17 or hour == 18:
        return time_list[9]
    elif hour == 19 or hour == 20:
        return time_list[10]
    elif hour == 21 or hour == 22:
        return time_list[11]


def get_lunar(date):
    # 获取当前日期的农历
    filename = '1901-2100_lunar.json'
    data_folder = os.path.dirname(os.getcwd()) + '\data'
    with open(f'{data_folder}\{filename}', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data[date]


def get_result(sum):
    return (sum - 2) % 6


def main():
    current_time = get_chinese_time(now)
    current_time_index = time_list.index(current_time)

    current_date = now.strftime("%Y-%m-%d")
    current_lunar = get_lunar(current_date)
    current_lunar_month = current_lunar['month']
    current_lunar_month_index = month_list.index(current_lunar_month)
    current_lunar_day = current_lunar['day']
    current_lunar_day_index = day_list.index(current_lunar_day)

    sum = current_lunar_month_index + current_lunar_day_index + current_time_index

    result = get_result(sum)

    print(
        f'{current_lunar_month}{current_lunar_day} {current_time}')
    print(f'{result_list[result]}')
    print(f'断曰：{gua_ci[result]}。')


if __name__ == "__main__":
    main()
