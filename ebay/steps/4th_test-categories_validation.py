###
# 4TH TEST - CATEGORIES VALIDATION

from behave import step
from selenium.webdriver.common.by import By


@step('Validate categories and subcategories are matching the table')
def categories_validation(context):
    # extracting expected categories from the table and creating a dictionary of sets for comparison
    expected_categories = {
        row['Category'].strip().lower(): set(sub.strip().lower() for sub in row['Subcategories'].split('; '))
        for row in context.table
    }
    # finding all categories on the page
    categories = context.driver.find_elements(By.XPATH, "//h3[contains(@class, 'gh-')][./following-sibling::ul]")
    actual_categories = {}
    # looping through each category found on the page
    for category in categories:
        category_name = category.text.strip().lower()
        print(f"⬇️ {category_name}")  # debug print to show the category being processed
        # finding all subcategory elements within this category
        subcategory_elements = category.find_elements(By.XPATH, "./following-sibling::ul[1]//a[@class='scnd']")
        subcategory_names = set(subcategory.text.strip().lower() for subcategory in subcategory_elements)
        actual_categories[category_name] = subcategory_names
        # debug prints for each subcategory
        for subcategory_name in subcategory_names:
            print(subcategory_name)
        print("*")
    # checking for unexpected and missing categories
    discrepancies = []
    unexpected_categories = set(actual_categories.keys()) - set(expected_categories.keys())
    missing_categories = set(expected_categories.keys()) - set(actual_categories.keys())
    if unexpected_categories or missing_categories:
        mismatch_message = ""
        if unexpected_categories:
            mismatch_message += f"Actual categories found: {unexpected_categories}\n"
        if missing_categories:
            mismatch_message += f"Expected categories: {missing_categories}"
        discrepancies.append(mismatch_message.strip())
    # validating categories and their subcategories
    for category, expected_subcategories in expected_categories.items():
        if category in actual_categories:
            # calculating subcategories that do not match
            missing_subcategories = expected_subcategories - actual_categories[category]
            extra_subcategories = actual_categories[category] - expected_subcategories
            # recording discrepancies for subcategories
            if missing_subcategories or extra_subcategories:
                subcategory_message = f"Subcategories for '{category}' do not match.\n"
                if missing_subcategories:
                    subcategory_message += f"   Expected: {missing_subcategories}\n"
                if extra_subcategories:
                    subcategory_message += f"   Actual: {extra_subcategories}"
                discrepancies.append(subcategory_message)
    # asserting if there are any discrepancies
    if discrepancies:
        assert False, "\nDiscrepancies found:\n" + "\n".join(discrepancies)
    else:
        print("✅ All categories and subcategories are matching perfectly!")


# @step('Click on All Categories dropdown')
# def click_all_categories_dropdown(context):
#     context.all_categories_dd = context.driver.find_element(
#         By. XPATH, f"//div[@id='gh-cat-box'][.//option[text()='All Categories']]").click()
#     context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
#     print("Clicked on All Categories dropdown")
#
#
# @step('Verify All Categories dropped down')
# def verify_all_categories_dropped_down(context):
#     class_attribute = context.all_categories_dd.get_attribute("class")
#     assert "gh-cat-box-focus" in class_attribute, "All Categories hasn't dropped down"
#     print("All categories has dropped down")
