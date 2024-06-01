###
# 2ND TEST - HEADER VALIDATION

from behave import step
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


@step('Verify "{page}" page has opened. Expected url: "{expected_url}"')
def compare_urls(context, page, expected_url):
    # ! enter name of the page & expected url to assert if current url is the expected one
    actual_url = context.driver.current_url
    assert expected_url in actual_url, \
        f"\nExpected URL to contain '{expected_url}', but got '{actual_url}'"
    print("✅", page, "page has successfully opened\n***")
    # try:
    #     # context.wait.until(lambda driver: expected_url in driver.current_url)
    # except TimeoutException:
    #     print("\033[91m ❌ Timeout occurred\033[0m\n***")
    # except Exception as e:
    #     print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")


@step('Click on "{link}"')
def click_header_link(context, link):
    header_link = context.driver.find_element(
        By.XPATH, f"//*[contains(@class,'gh-') and contains(text(), '{link}')] | "
        f"//*[contains(@class,'gh-')]/child::a[contains(text(), '{link}')] | "
        f"//*[contains(@class,'gh-')]/span/child::a[contains(text(), '{link}')] | "
        f"//*[contains(@class,'gh-') and contains(text(), '{link}')]/preceding-sibling::a"
    )
    header_link.click()
    print("✅ Clicked on", link)


@step('Hover over {link} element')
def hover(context, link):
    header_element = context.driver.find_element(
        By.XPATH, f"//*[contains(@class,'gh-') and text() = '{link}'] | "
                  f"//*[contains(@class,'gh-') and contains(text(), '{link}')]/preceding-sibling::a | "
                  f"//button[contains(@title, '{link}')] | "
                  f"//button[contains(text(), '{link}')][@aria-expanded]"
    )
    context.actions.move_to_element(header_element).perform()
    if header_element.find_element(By.XPATH,
                                   "./following-sibling::a[@aria-expanded] | "
                                   "./parent::button[@aria-expanded] | "
                                   "./self::button[@aria-expanded]"
                                   ).get_attribute("aria-expanded") == "true":
        print("✅ Hovered over", link, "element")
    else:
        # if hovering didn't work, click on the element
        header_element.click()
        print("✅ Clicked on", link, "element")


def attribute_to_be(locator, attribute, value):
    def _wait(driver):
        element = driver.find_element(*locator)
        return element.get_attribute(attribute) == value
    return _wait


@step('Verify {dropdown_element} dropdown')
def verify_dropdown_element(context, dropdown_element):
    try:
        context.wait.until(
            attribute_to_be(
                (By.XPATH,
                 f"//*[contains(@class,'gh-') and text() = '{dropdown_element}']"
                 f"/following-sibling::a[@aria-expanded] | "
                 f"//*[contains(@class,'gh-') and text() = '{dropdown_element}']"
                 f"/parent::button[@aria-expanded] | "
                 f"//*[contains(@class,'gh-') and contains(text(), '{dropdown_element}')][@aria-expanded] | "
                 f"//button[contains(@title, '{dropdown_element}')]"),
                "aria-expanded", "true"))
        print("✅", dropdown_element, "has successfully dropped down\n***")
    except TimeoutException:
        print("\033[91m ❌ Timeout occurred\033[0m\n***")
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
