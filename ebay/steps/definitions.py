from behave import step
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
# from warnings import warn
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


# 4TH TEST - CATEGORIES VALIDATION
@step('The categories and subcategories should be:')
def step_impl(context):
    # extracting expected categories from context.table
    expected_categories = {row['Category']: row['Subcategories'].split('; ') for row in context.table}
    print("1")
    categories = context.driver.find_elements(By.XPATH, "//h3[contains(@class, 'gh-')][./following-sibling::ul]")
    print("2")
    actual_categories = {}
    for category in categories:
        print(category.text)
        category_name = category.text.strip()
        subcategory_elements = category.find_elements(By.XPATH, "//a[@class='scnd']")
        subcategory_names = [subcategory.text.strip() for subcategory in subcategory_elements]
        actual_categories[category_name] = subcategory_names
    for category, subcategories in expected_categories.items():
        assert category in actual_categories, f"Category '{category}' not found"
        assert set(actual_categories[category]) == set(
            subcategories), f"Subcategories for '{category}' do not match. Expected {subcategories}, but got {actual_categories[category]}"


# 3RD TEST - FILTER VALIDATION
@step('Filter by "{section}", choose subsection "{subsection}" and select "{filter_value}"')
def filter_by_value(context, section, subsection, filter_value):
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


# 2ND TEST - HEADER VALIDATION
@step('Verify "{page}" page has opened. Expected url: "{expected_url}"')
def compare_urls(context, page, expected_url):
    # ! enter name of the page & expected url to assert if current url is the expected one
    actual_url = context.driver.current_url
    assert expected_url in actual_url, \
        f"Expected URL to contain '{expected_url}', but got '{actual_url}'"
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
    sleep(1)


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


###
# 1ST TEST - DRESS SEARCH
@step('Enter "{search_text}" into the searchbar')
def enter_dress(context, search_text):
    searchbar = context.driver.find_element(By.XPATH, "//input[@aria-label='Search for anything']")
    searchbar.send_keys(f"{search_text}")
    print(f"✅ Entered '{search_text}' into the search bar\n***")


@step('Click on "Search" button')
def click_search_button(context):
    search_button = context.driver.find_element(By.XPATH, "//input[@id='gh-btn']")
    search_button.click()
    print("✅ Clicked on 'Search' button\n***")
    #   waiting until 1st dress is loaded and visible
    context.first_dress = context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "(//div[@class='s-item__image-wrapper image-treatment'])[2]")
        )
    )
    print("✅ Results page has loaded\n***")


@step('Click on the first dress')
def click_first_dress(context):
    initial_handles = context.driver.window_handles
    current_handle = context.driver.current_window_handle
    context.first_dress.click()
    print("✅ Clicked on the first dress\n***")
    updated_handles = context.driver.window_handles
    if len(updated_handles) > len(initial_handles):
        print("✅ A new tab with the product has opened\n***")
    else:
        print("❌ No new tab has been opened\n***")
    #   switching to a newly opened tab
    for handle in context.driver.window_handles:
        if handle != current_handle:
            context.driver.switch_to.window(handle)
            break
    print("✅ Opened product:", context.driver.title, "\n***")
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//a[@id='binBtn_btn_1']")
        )
    )
    print("✅ Product page has loaded\n***")
    product_title_el = context.driver.find_element(
        By.XPATH, "//h1[@class='x-item-title__mainTitle']/span"
    )
    # storing product title to compare in the next step if this item was added to the cart
    context.product_title = product_title_el.text


@step('Click "Add to cart button"')
def click_add_to_cart_button(context):
    context.add_to_cart_btn = context.driver.find_element(
        By.XPATH, "//a[@id='atcBtn_btn_1']"
    )
    context.add_to_cart_btn.click()
    print("✅ Clicked 'Add to cart' button\n***")
    context.wait.until(ec.visibility_of_element_located(
        (By.XPATH, "//div[@class='ux-layout-section__row']//span[text()='Go to cart']")))
    print("✅ Lightbox has opened, product has been added to the cart\n***")


@step('Click "Go to cart"')
def click_go_to_cart(context):
    context.go_to_cart_btn = context.driver.find_element(
        By.XPATH, "//div[@class='ux-layout-section__row']//span[text()='Go to cart']"
    )
    context.go_to_cart_btn.click()
    print("✅ Clicked 'Go to cart' button\n***")
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//button[text()='Go to checkout']")
        )
    )
    print("✅ Cart has opened\n***")


@step('Verify the item was added to the cart')
def click_sell_button(context):
    try:
        context.wait.until(
            ec.text_to_be_present_in_element((By.XPATH, "//div[@data-test-id='app-cart']"), context.product_title)
        )
        print("✅ Item was successfully added to the cart")
    except TimeoutException:
        print("❌ Timeout\n**")
    except Exception as e:
        print("❌", e)

# @step('Verify all items on {number_of_pages} pages are related to "{desired_title}"')
# def check_all_item_titles(context, number_of_pages, desired_title):
#     number_of_pages = int(number_of_pages)
#     issues = []
#     page_count = 1
#     number_of_issues = 0
#     while page_count <= number_of_pages:
#         all_items = context.driver.find_elements(By.XPATH, "//li[contains(@id, 'item')]//span[@role='heading']")
#         item_count = 0
#         print("✅ Page #", page_count)
#         for item in all_items:
#             title = item.text
#             item_count += 1
#             print(item_count, title)
#             if desired_title.lower() not in title.lower():
#                 issues.append(f'{title} is not "{desired_title}" related')
#                 number_of_issues += 1
#         context.next_page = context.driver.find_element(By.XPATH, "//a[@aria-label='Go to next search page']").click()
#         context.wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
#         page_count += 1
#     if issues:
#         raise Exception(f'Following {number_of_issues} issues discovered:\n{"\n".join(issues)}')
