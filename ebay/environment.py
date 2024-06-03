from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import os
import re


def before_all(context):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1920, 1080)
    context.wait = WebDriverWait(context.driver, 30)
    context.actions = ActionChains(context.driver)
    print("✅ Browser instance is successfully initiated\n***")


def after_step(context, step):
    if step.status == 'failed':
        # sanitizing step name
        step_name = re.sub(r'[\W_]+', '_', step.name)
        current_dir = os.path.dirname(__file__)
        screenshots_dir = os.path.abspath(os.path.join(current_dir, 'screenshots'))
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        context.driver.save_screenshot(os.path.join(screenshots_dir, f"{step_name}.png"))
        print(f"***\n📷 Screenshot saved: {step_name}", end='')


def after_all(context):
    context.driver.quit()
    print("✅ Browser has closed")
