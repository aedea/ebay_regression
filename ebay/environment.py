from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


def before_all(context):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1920, 1080)
    context.wait = WebDriverWait(context.driver, 30)
    context.actions = ActionChains(context.driver)
    context.driver.implicitly_wait(30)
#    context.browser_initialized = True
    print("✅ Browser has successfully opened\n***")


"""    
def before_scenario(context, scenario):
    if not context.browser_initialized:
        context.driver.implicitly_wait(30)
        context.browser_initialized = True
"""


def after_all(context):
    context.driver.quit()
