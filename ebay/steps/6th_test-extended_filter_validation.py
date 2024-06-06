
# 6TH TEST - EXTENDED FILTER VALIDATION

from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@step('Validate that all items are relevant to the applied filter')
def filter_validation(context):
    all_items = context.driver.find_elements(By.XPATH, "//li[contains(@id, 'item')][//span[@role='heading']]")
    initial_window = context.driver.current_window_handle  # getting id of the current tab
    # issues = []
    cycle_issues = []
    item_count = 0
    issue_count = 0
    for item in all_items:
        item_count += 1
        title = item.find_element(By.XPATH, ".//span[@role='heading']").text
        product_url = item.find_element(By.XPATH, ".//a[@class='s-item__link']").get_attribute('href')
        # get to the item page
        context.driver.execute_script(f"window.open('{product_url}');")  # open urls from product_url
        context.driver.switch_to.window(context.driver.window_handles[-1])  # switch to the latest tab
        # collect item spec
        item_labels = context.wait.until(
            ec.presence_of_all_elements_located((
                By.XPATH, "//dt[@class='ux-labels-values__labels']//span")))
        item_values = context.wait.until(
            ec.presence_of_all_elements_located((
                By.XPATH, "//dd[@class='ux-labels-values__values']//div[@class='ux-labels-values__values-content']")))
        # get text from items
        item_labels_text = []
        for label in item_labels:
            item_labels_text.append(label.text)
        item_values_text = []
        for value in item_values:
            item_values_text.append(value.text)
        item_specs = dict(zip(item_labels_text, item_values_text))  # dict        # the validation
        if context.filter_section or context.filter_subsection not in item_specs.keys():
            # issues.append(f"{title} doesnt have anything related to {context.filter_section}")
            cycle_issues.append(f"doesnt have anything related to {context.filter_section}")
        if item_specs[context.filter_section] != context.filter_value:
            cycle_issues.append(f"doesnt have anything related to {context.filter_section}")
            # issues.append(f" Not related to {context.filter_value} by {context.filter_section} "

        print("🛈 Checked product №", item_count, "/", len(all_items))
        if cycle_issues:
            print(f'Title:, {title} \n URL: {product_url} \n Found issues:\n{"\n".join(cycle_issues)}')
        cycle_issues = []
        # close tab
        context.driver.close()
        context.driver.switch_to.window(initial_window)
    # if issues:
    #     raise Exception(f'Following issues discovered:\n{"\n".join(issues)}')
