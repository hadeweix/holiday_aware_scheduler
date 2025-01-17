import importlib
from datetime import timedelta

import pandas as pd
from tabulate import tabulate


# 动态加载节假日和调休日
def load_holidays():
    holidays = {}
    holidays_module = importlib.import_module("holidays")
    for attr in dir(holidays_module):
        if attr.startswith("HOLIDAYS_"):
            year = int(attr.split("_")[1])
            holidays[year] = {
                "holidays": getattr(holidays_module, attr),
                "leave_in_lieu": getattr(holidays_module, f"LEAVE_IN_LIEU_{year}", []),
            }
    return holidays


# 获取节假日数据
ALL_HOLIDAYS = load_holidays()


def get_holidays(year):
    """根据年份获取节假日和调休日，若无数据直接抛出异常"""
    if year not in ALL_HOLIDAYS:
        raise ValueError(f"找不到 {year} 年的假期数据 请更新 'holidays.py'")
    return ALL_HOLIDAYS[year]


def is_working_day(date):
    """判断是否为工作日（非周末且非假期，或为调休）"""
    holidays_data = get_holidays(date.year)
    holidays = holidays_data["holidays"]
    leave_in_lieu = holidays_data["leave_in_lieu"]

    # 调休日优先级高于周末和节假日
    if date in leave_in_lieu:
        return True
    return date.weekday() < 5 and date not in holidays


def schedule_tasks(tasks, start_date):
    """
    根据任务列表和起始日期生成任务调度表
    :param tasks: 每个任务的工作量（以工作日为单位）的列表
    :param start_date: 起始日期
    :return: 调度计划（列表形式）
    """
    schedule = []
    current_date = start_date

    for workload in tasks:
        # 确保任务的开始时间是工作日
        while not is_working_day(current_date):
            current_date += timedelta(days=1)
        start = current_date

        # 分配工作量
        days_needed = workload
        while days_needed > 0:
            if is_working_day(current_date):
                days_needed -= 1
            if days_needed > 0:  # 确保任务未完成时才推进日期
                current_date += timedelta(days=1)

        # 确定结束时间
        end = current_date
        while not is_working_day(end):  # 校正为工作日
            end += timedelta(days=1)

        # 保存当前任务的计划
        schedule.append({
            "工作量(单位：天)": workload,
            "计划开始日期": start.strftime("%Y/%m/%d"),
            "计划结束日期": end.strftime("%Y/%m/%d")
        })

        # 确保下一任务的开始时间从有效的工作日开始
        current_date = end + timedelta(days=1)
        while not is_working_day(current_date):
            current_date += timedelta(days=1)

    return schedule


def save_schedule_to_csv(schedule, file_name):
    """保存调度计划到 CSV 文件"""
    schedule_df = pd.DataFrame(schedule)
    schedule_df.to_csv(file_name, index=False, encoding="utf-8-sig")
    print(f"Schedule saved to {file_name}")
    return schedule_df


def display_schedule(schedule):
    """以 Markdown 表格形式显示调度计划"""
    schedule_df = pd.DataFrame(schedule)
    print(tabulate(schedule_df, headers="keys", tablefmt="pipe", showindex=True, numalign="left", stralign="left"))
