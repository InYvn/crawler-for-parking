from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tkinter import messagebox
import time
from datetime import datetime

def send_popup_notification(title, message):
    messagebox.showinfo(title, message)


def stopcar():
    # 设置 Chrome 选项
    options = webdriver.ChromeOptions()
    # 添加参数，模拟正常浏览器行为，避免被检测到是爬虫
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')  # 最大化窗口
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # 可选，提升兼容性

    # 创建 Chrome 浏览器实例
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 打开目标网页
    driver.get('')

    # 等待10秒，确保页面加载完成
    time.sleep(6)

    # 获取网页内容
    page_source = driver.page_source
    print(page_source)

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

    for text in all_texts:
        print(text)

    # 检查是否有“未停车”关键字
    if not any("未停车" in text for text in all_texts):
        send_popup_notification("注意", "目前停车中！")

    if any("停车中" in text for text in all_texts):
        send_popup_notification("注意", "目前停车中！")

    with open('baidu.html', 'w', encoding='utf-8') as f:
        f.write(page_source)

    # 等待6秒，确保页面加载完成
    driver.quit()


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