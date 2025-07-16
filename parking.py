from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tkinter import messagebox
import time
from datetime import datetime, timedelta
import re

def send_popup_notification(title, message):
    messagebox.showinfo(title, message)

def time_difference(text):
    text = "\n".join(text)
    # 提取第一个日期时间
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    match = re.search(pattern, text)
    if match:
        date_str = match.group()
        date_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - date_time
        hours, remainder = divmod(diff.total_seconds(), 3600)
        minutes = remainder // 60
        # 计算与1小时30分钟的差值
        total_minutes = int(hours) * 60 + int(minutes)
        target_minutes = 90  # 1小时30分钟
        delta_minutes = abs(total_minutes - target_minutes)
        delta_hours = delta_minutes // 60
        delta_remain_minutes = delta_minutes % 60
        # 停车结束时间
        end_time = date_time + timedelta(minutes=90)
        return (
            f"当前停车开始时间：{date_str}",
            f"停车结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"与当前时间相差：{int(hours)}小时{int(minutes)}分钟",
            f"与1小时30分钟相差：{int(delta_hours)}小时{int(delta_remain_minutes)}分钟"
        )
    else:
        return "未找到日期时间", "", "", ""


def stopcar():
    # 设置 Chrome 选项
    options = webdriver.ChromeOptions()
    # 添加参数，模拟正常浏览器行为，避免被检测到是爬虫
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')  # 最大化窗口
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # 可选，提升兼容性

    # 创建 Chrome 浏览器实例
    # https://googlechromelabs.github.io/chrome-for-testing/
    # 可选从网络自动下载 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 打开目标网页
    driver.get(
        '')

    # 等待10秒，确保页面加载完成
    time.sleep(6)

    # 获取网页内容
    page_source = driver.page_source
    # print(page_source)

    # 获取页面上的所有元素
    all_elements = driver.find_elements(By.XPATH, '//*')

    all_texts = []
    for el in all_elements:
        try:
            text = el.text.strip()
            if text:
                all_texts.append(text)
        except Exception:
            continue  # 跳过失效元素

    # for text in all_texts:
        # print(text)

    # 检查是否有“未停车”关键字
    if not any("未停车" in text for text in all_texts):
        time_diff1, time_diff2, time_diff3, time_diff4 = time_difference(all_texts)
        result_msg = "目前停车中！\n" + time_diff1 + "\n" + time_diff2 + "\n" + time_diff3 + "\n" + time_diff4
        send_popup_notification("注意", result_msg)
        print(f"停车检查时间：{current_time}, 检测到停车，停车结果：{result_msg}")
    elif any("停车中" in text for text in all_texts):
        time_diff1, time_diff2, time_diff3, time_diff4 = time_difference(all_texts)
        result_msg = "目前停车中！\n" + time_diff1 + "\n" + time_diff2 + "\n" + time_diff3 + "\n" + time_diff4
        send_popup_notification("注意", result_msg)
        print(f"停车检查时间：{current_time}, 检测到停车，停车结果：{result_msg}")
    else:
        print(f"停车检查时间：{current_time}, 未检测到停车。")

    with open('baidu.html', 'w', encoding='utf-8') as f:
        f.write(page_source)

    # 等待6秒，确保页面加载完成
    driver.quit()

now = datetime.now()
current_time = now.strftime("%H:%M")
stopcar()
print(f"首次启动，已执行一次停车检查。")

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_hour = int(now.strftime("%H"))
    current_minute = int(now.strftime("%M"))

    # 判断时间是否在 8:00 - 19:05 范围内，并且是整点
    if 8 <= current_hour <= 19:
        if current_minute == 0:
            stopcar()
            print(f"停车检查时间：{current_time},停车检查已完成，等待下一个整点...")
            # 等待到下一个整点
            time.sleep(60 - datetime.now().second)
            # 再多等待 55 分钟，确保下一次循环等待到下一个整点
            time.sleep(55 * 60)