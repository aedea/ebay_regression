from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import os


def before_scenario(context, scenario):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1920, 1080)
    context.wait = WebDriverWait(context.driver, 30)
    context.actions = ActionChains(context.driver)
    print("✅ Browser has successfully opened\n***")


def after_step(context, step):
    if step.status == 'failed':
        current_dir = os.path.dirname(__file__) # where this file located
        relative_path_to_dest = os.path.abspath(os.path.join(current_dir, 'failed_screenshots'))
        context.driver.save_screenshot(os.path.join(relative_path_to_dest, f'{step.name}.png'))


def after_scenario(context, scenario):
    context.driver.quit()
    print("✅ Browser has closed")
