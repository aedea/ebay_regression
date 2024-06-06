###
# 3RD TEST - FILTER VALIDATION

from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import warnings


@step('Filter by "{section}", choose subsection "{subsection}" and select "{filter_value}"')
def filter_by_value(context, section, subsection, filter_value):
    context.filter_section = section
    context.filter_subsection = subsection
    context.filter_value = filter_value
    filter_section = context.driver.find_element(By.XPATH, f"//li[@class = 'x-refine__main__list ']"
                                                           f"[.//div[text() = '{section}']]")
    if filter_section.get_attribute("aria-expanded") == "false":
        filter_section.click()
    if subsection != "NONE":
        filter_subsection = filter_section.find_element(By.XPATH, f".//div[./h4[text()='{subsection}']]")
        if filter_subsection.get_attribute("aria-expanded") == "false":
            filter_subsection.click()
        subsection_select = filter_section.find_element(
            By.XPATH, f".//div[@class='size-component'][.//h4[text()='{subsection}']]//span[text()='{filter_value}']")
        subsection_select.click()
        context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Filtered by '"+section+"', '"+subsection+"', '"+filter_value+"'\n***")
    else:
        filter_check = filter_section.find_element(
            By.XPATH, f".//div[@class='x-refine__select__svg'][.//span[text()='{filter_value}']]//input | "
                      f".//span[text()='{filter_value}']/parent::a"
        )
        filter_check.click()
        context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
        print("✅ Filtered by '"+section+"' and selected '"+filter_value+"'\n***")


def validate_titles(context, initial_page, desired_title):
    all_items = context.driver.find_elements(By.XPATH, "//li[contains(@id, 'item')]//span[@role='heading']")
    item_count = 0
    print("⬇️ Page #", initial_page)
    for item in all_items:
        title = item.text
        item_count += 1
        print(item_count, title)
        if desired_title.lower() not in title.lower():
            context.issues.append(f'{title} is not "{desired_title}" related')
            context.number_of_issues += 1


@step('Verify all titles from page №{initial_page} to page №{desired_page} are related to "{desired_title}"')
def check_all_item_titles(context, initial_page, desired_page, desired_title):
    context.driver.find_element(By.XPATH, f"//a[@class='pagination__item'][text()='{initial_page}']").click()
    context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
    context.number_of_issues = 0
    context.issues = []
    initial_page = int(initial_page)
    desired_page = int(desired_page)
    if initial_page != desired_page:
        while initial_page != desired_page:
            validate_titles(context, initial_page, desired_title)
            if initial_page < desired_page:
                context.next_page = context.driver.find_element(By.XPATH,
                                                                "//a[@aria-label='Go to next search page']").click()
                context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
                print('✅ Clicked next page button')
                initial_page += 1
            else:
                context.next_page = context.driver.find_element(By.XPATH,
                                                                "//a[@aria-label='Go to previous search page']").click()
                context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
                print('✅ Clicked previous page button')
                initial_page -= 1
    validate_titles(context, initial_page, desired_title)
    if context.issues:
        raise Exception(f'Following {context.number_of_issues} issues discovered:\n{"\n".join(context.issues)}')


@step('Go to page #{search_page}')
def go_to_page(context, search_page):
    context.driver.find_element(By.XPATH, f"//li[a[@class='pagination__item' and text()='{search_page}']]").click()
    context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
    print("Went to page #", search_page)
