
# 6TH TEST - EXTENDED FILTER VALIDATION

from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


@step('Validate that all items are relevant to the applied filter')
def filter_validation(context):
    all_items = context.driver.find_elements(By.XPATH, "//li[contains(@id, 'item')][//span[@role='heading']]")
    initial_window = context.driver.current_window_handle  # getting id of the current tab
    issues = []
    all_issues = []
    item_count = 0
    issue_count = 0
    for item in all_items:
        item_count += 1
        # title = item.find_element(By.XPATH, ".//span[@role='heading']").text
        product_url = item.find_element(By.XPATH, ".//a[@class='s-item__link']").get_attribute('href')
        # get to the item page
        context.driver.execute_script(f"window.open('{product_url}');")  # opening urls from product_url
        context.driver.switch_to.window(context.driver.window_handles[-1])  # switching to the latest tab
        # collecting item specs
        item_labels = context.wait.until(
            ec.presence_of_all_elements_located((
                By.XPATH, "//dt[@class='ux-labels-values__labels']//span")))
        item_values = context.wait.until(
            ec.presence_of_all_elements_located((
                By.XPATH, "//dd[@class='ux-labels-values__values']//div[@class='ux-labels-values__values-content']")))
        # getting text from items and creating dictionary
        item_labels_text = []
        for label in item_labels:
            item_labels_text.append(label.text)
        item_values_text = []
        for value in item_values:
            item_values_text.append(value.text)
        item_specs = dict(zip(item_labels_text, item_values_text))
        # validation
        if context.filter_section.lower() not in [k.lower() for k in item_specs.keys()]:
            issue_count += 1
            issues.append(f"The product doesn't have '{context.filter_section}' specification")
            all_issues.append(f"{issue_count}) The product doesn't have '{context.filter_section}' specification\n"
                              f"Product URL: {product_url}\n")
        elif item_specs[context.filter_section].lower() != context.filter_value.lower():
            issue_count += 1
            issues.append(f"The '{context.filter_section}' doesn't match '{context.filter_value}'. "
                          f"Actual value: '{item_specs[context.filter_section]}'")
            all_issues.append(f"{issue_count}) The '{context.filter_section}' doesn't match '{context.filter_value}'. "
                              f"Actual value: '{item_specs[context.filter_section]}'\n"
                              f"Product URL: {product_url}\n")
        print("🛈 Checked product №", item_count, "/", len(all_items), ": ", end='')
        context.driver.close()
        context.driver.switch_to.window(initial_window)
        if issues:
            print(f'❌\nFound issues:\n{"\n".join(issues)}\nURL: {product_url}')
        else:
            print("✅")
        issues = []
    if all_issues:
        raise Exception(f'Found {issue_count} issues:\n{"\n".join(all_issues)}')
