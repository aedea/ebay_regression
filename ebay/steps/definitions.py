from behave import step
from selenium.common import TimeoutException, NoSuchElementException
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


# 5TH TEST - BANNER VALIDATION
@step('Make sure the banner is visible')
def banner_visibility(context):
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//div[@aria-roledescription='Carousel'][.//div[@class='tracking-wrapper']]")),
        message="❌ Banner isn't visible\n***"
    )
    print("✅ Banner is visible\n***")
    context.banner_slides = context.driver.find_elements(
        By.XPATH, "//li[@class='carousel__snap-point vl-carousel__item'][div[@class='tracking-wrapper']]")


def get_active_slide_index(context):
    for i, slide in enumerate(context.banner_slides):
        if slide.get_attribute("aria-hidden") is None:
            return i
    return None


def check_slide_transition(context):
    expected_next_slide = (context.initial_slide_index + 1) % len(context.banner_slides)
    new_active_slide_index = get_active_slide_index(context)
    if new_active_slide_index == expected_next_slide:
        print(f"🛈 Transitioned to slide № {new_active_slide_index + 1}")
        context.initial_slide_index = new_active_slide_index  # next iteration update
        return True
    else:
        print("❌ Slide transition failed\n***")
        return False


def wait_for_slide_transition(context):
    context.wait.until(
        lambda driver:
        get_active_slide_index(context) == (context.initial_slide_index + 1) % len(context.banner_slides)
    )


@step('Validate the banner is spinning by default')
def auto_banner_spin(context):
    context.initial_slide_index = get_active_slide_index(context)
    print(f"🛈 Initial slide № {context.initial_slide_index + 1} is visible")
    try:
        wait_for_slide_transition(context)
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
    print("✅ Banner is spinning\n***")


@step('Validate {number_of_spins} banner transitions')
def banner_spinning(context, number_of_spins):
    successful_transitions = 0
    for _ in range(int(number_of_spins)):
        try:
            wait_for_slide_transition(context)
            if check_slide_transition(context):
                successful_transitions += 1
        except Exception as e:
            print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
    print(f"✅ Banner has successfully made {successful_transitions} transitions\n***")


# 4TH TEST - CATEGORIES VALIDATION
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
            (By.XPATH, "(//div[@class='s-item__image-wrapper image-treatment'])[3]")
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
        print("✅ Item was successfully added to the cart\n***")
    except TimeoutException:
        print("❌ Timeout\n**")
    except Exception as e:
        print("❌", e)
