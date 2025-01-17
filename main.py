from datetime import datetime

from scheduler import schedule_tasks, display_schedule, save_schedule_to_csv

try:
    # 配置任务和起始日期
    tasks = [3, 4, 1, 1]  # 每个任务的工作量（工作日数）
    start_date = datetime.strptime("2025-04-02", "%Y-%m-%d")  # 起始日期
    # 调用调度函数
    schedule = schedule_tasks(tasks, start_date)
    # 显示和保存调度计划
    display_schedule(schedule)  # 显示计划
    save_schedule_to_csv(schedule, "task_schedule.csv")  # 保存到 CSV 文件
except ValueError as e:
    print(f"Error: {e}")
