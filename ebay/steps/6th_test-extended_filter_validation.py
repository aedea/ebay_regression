
#

from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@step('Validate that all "{search_title}" "{key_name}" are "{expected_value}"')
def filter_validation(context, search_title):
    all_items = context.driver.find_elements(By.XPATH, "//li[contains(@id, 'item')]//span[@role='heading']")
    initial_window = context.driver.current_window_handle #getting id of the current tab
    wait = WebDriverWait(context.driver, 5)
    issues = []
    for item in all_items:
        title = item.find_element(By.XPATH, ".//span[@role='heading'].text")  # check if works
        product_url = item.find_element(By.XPATH, ".//a[@class='s-item__link']").get_attribute('href')
        #get to the item page
        context.driver.execute_script(f"window.open({'product_url'};)")
        context.driver.switch_to.window(context.driver.window_handles[-1]) #switch to the latest tab
        #click
        #switch
        #collect item spec
        all_labels = context.driver.find_elements(By.XPATH, "//dt[@class='ux-labels-value__labels']")
        all_values = context.driver.find_elements(By.XPATH, "//dd[@class='ux-labels-value__values']")
        #get text from items
        all_labels_text = []
        for label in all_labels:
            all_labels_text.append(label.text)
            all_values_text=[]
            for value in all_values:
                all_values_text.append(value.text)
                item_specs = dict(zip(all_labels_text, all_values_text)) #dict
                #do the validation
                if key_name not in item_specs.keys():
                    issues.append(f"{title} doesnt have anything related to {key_name}")
                if item_specs[key_name] != expected_value:
                    issues.append(f"{title} is not related to {expected_value} by {key_name}")


#switch back

context.driver.switch_to.window(initial_window)

if issues: