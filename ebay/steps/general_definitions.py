from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


@step('Go to "{url}"')
def go_to_url(context, url):
    try:
        context.driver.get("https://"+url)
        context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
        # line below is ONLY FOR EBAY.COM due to captcha and kicking out
        context.wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id='gh-l-h1']")))
        print("✅ Went to", url, "\n***")
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")


@step('Wait {sec} seconds')
def wait(context, sec):
    sleep(int(sec))
