# 停车计费监测工具

## 项目简介
本项目是一个基于Selenium的网页数据监测工具，可定时监控指定网页的停车状态信息。通过无头浏览器模式实现静默运行，支持在检测到异常状态时自动弹窗提醒，适用于需要长期监控网页数据的场景。

## 功能特性
- ✅ **定时任务**：每日8:00-19:00整点自动执行监测
- 🕵️ **无头模式**：后台静默运行不干扰用户操作
- 💡 **状态监测**：自动检测"停车状态"或异常未返回状态
- 🚨 **即时提醒**：检测到异常时触发系统弹窗通知
- 🔄 **可扩展性**：通过修改URL即可适配其他网页监控需求

## 技术依赖
Python 3.12
selenium>=4.0.0
webdriver-manager>=3.8.0

## 使用说明

### 1. 修改监控网址

请在 `parking.py` 文件中找到如下代码，并将目标网址替换为你需要监控的实际地址：

```python
driver.get('https://your-target-url.com/parking')  # 替换为实际监控地址
```

### 2\. 配置 ChromeDriver

- 推荐将 `chromedriver` 放在项目根目录，或使用 `webdriver-manager` 自动下载和管理驱动。
- 也可前往 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载与你浏览器版本对应的 `chromedriver`。

### 3\. 确认 Chrome 浏览器版本

确保 `chromedriver` 版本与本地 Chrome 浏览器主版本号一致，否则可能无法正常运行。

**查看本地 Chrome 版本方法：**
1. 打开 Chrome 浏览器
2. 在地址栏输入 `chrome://settings/help` 或 `chrome://version/`
3. 记下主版本号（如 `114.0.5735.90`，主版本号为 `114`）

如有版本不匹配，请下载对应版本的 `chromedriver`。

## 注意事项

❗ **合法合规声明**：

- 请确保目标网站允许自动化访问
- 遵守《网络安全法》及网站robots.txt协议
- 建议与网站管理员沟通获取授权