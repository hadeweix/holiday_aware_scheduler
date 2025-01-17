from datetime import datetime

from scheduler import schedule_tasks, display_schedule, save_schedule_to_csv

try:
    # 每个任务的工作量（工作日数）
    tasks = [3, 4, 1, 1, 3, 4, 1, 13, 4, 1, 1, 3, 5, 6]
    # 起始日期
    start_date = datetime.strptime("2025-04-02", "%Y-%m-%d")
    # 调用调度函数
    schedule = schedule_tasks(tasks, start_date)
    # 显示计划
    display_schedule(schedule)
    # 保存到 CSV 文件
    save_schedule_to_csv(schedule, "task_schedule.csv")
except ValueError as e:
    print(f"Error: {e}")
