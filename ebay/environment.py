from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


def before_all(context):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1920, 1080)
    context.wait = WebDriverWait(context.driver, 30)
    context.actions = ActionChains(context.driver)
    print("✅ Browser has successfully opened\n***")


def after_all(context):
    context.driver.quit()
    print("✅ Browser has closed")
