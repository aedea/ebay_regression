from behave import step
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


def wait_for_element_by_xpath(driver, xpath, timeout=13):
    # ! enter xpath to wait for the element to be loaded
    try:
        WebDriverWait(driver, timeout).until(
            ec.visibility_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException:
        print("\033[91m !Timeout occurred: Element not found\033[0m")
    except Exception as e:
        print("\033[91m !An error occurred:\033[0m", e)


def compare_urls(driver, expected_url, name_of_element):
    # ! enter (expected url, name of element) to compare if current url is the expected one
    # ! also put the name of the element being tested
    current_url = driver.current_url
    if current_url == expected_url:
        print(name_of_element, " has successfully opened\n***")
    else:
        print("\033[91m", name_of_element, "has NOT opened !\033[0m\n***")


def check_dropdown(driver, xpath, name_of_element):
    # ! enter xpath for dropdown and the name
    dropdown_exp = driver.find_element(By.XPATH, xpath)
    aria_exp_value = dropdown_exp.get_attribute("aria-expanded")
    if aria_exp_value == "true":
        print(name_of_element, "has been expanded\n***")
    else:
        print("\033[91m", name_of_element, "has NOT expanded !\033[0m\n***")


@step('Open Chrome')
def open_chrome(context):
    context.driver = webdriver.Chrome()
    context.wait = WebDriverWait(context.driver, 13)
    context.actions = ActionChains(context.driver)
    print("Browser has successfully opened\n***")


@step('Navigate to eBay.com')
def navigate_to_ebay(context):
    context.driver.get("https://ebay.com")
    #   waiting until logo has loaded
    wait_for_element_by_xpath(context.driver, "//img[@id='gh-logo' and @alt='eBay Home']")
    print("Navigated to ebay.com\n***")


@step('Enter "dress" to the searchbar')
def enter_dress(context):
    searchbar = context.driver.find_element(By.XPATH, "//input[@aria-label='Search for anything']")
    searchbar.send_keys("dress")
    print("Entered 'dress' into the search bar\n***")


@step('Click on "Search" button')
def click_search_button(context):
    search_button = context.driver.find_element(By.XPATH, "//input[@id='gh-btn']")
    search_button.click()
    print("Clicked on 'Search' button\n***")
    #   waiting until 1st dress is loaded and visible
    context.first_dress = context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "(//div[@class='s-item__image-wrapper image-treatment'])[2]")
        )
    )
    print("Page has loaded\n***")


@step('Click on the first dress')
def click_first_dress(context):
    initial_handles = context.driver.window_handles
    current_handle = context.driver.current_window_handle
    context.first_dress.click()
    print("Clicked on the first dress\n***")
    updated_handles = context.driver.window_handles
    if len(updated_handles) > len(initial_handles):
        print("A new tab has opened.\n***")
    else:
        print("No new tab has been opened.\n***")
    #   switching to a newly opened tab
    for handle in context.driver.window_handles:
        if handle != current_handle:
            context.driver.switch_to.window(handle)
            break
    print("Opened product:", context.driver.title, "\n***")
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//a[@id='binBtn_btn_1']")
        )
    )
    print("'Buy It Now' button is shown, page is loaded\n***")
    product_title_el = context.driver.find_element(
        By.XPATH, "//h1[@class='x-item-title__mainTitle']/span"
    )
    context.product_title = product_title_el.text


@step('Click "Add to cart button"')
def click_add_to_cart_button(context):
    context.add_to_cart_btn = context.driver.find_element(
        By.XPATH, "//a[@id='atcBtn_btn_1']"
    )
    context.add_to_cart_btn.click()
    print("Clicked 'Add to cart' button\n***")
    wait_for_element_by_xpath(context.driver, "//div[@class='ux-layout-section__row']//span[text()='Go to cart']")
    """
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//div[@class='ux-layout-section__row']//span[text()='Go to cart']")
        )
    )
    """
    print("Lightbox has opened\n***")


@step('Click "Go to cart"')
def click_go_to_cart(context):
    context.go_to_cart_btn = context.driver.find_element(
        By.XPATH, "//div[@class='ux-layout-section__row']//span[text()='Go to cart']"
    )
    context.go_to_cart_btn.click()
    print("Clicked 'Go to cart' button\n***")
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//button[text()='Go to checkout']")
        )
    )
    print("Cart is opened\n***")


@step('Verify the item was added to the cart')
def click_sell_button(context):
    try:
        context.wait.until(
            ec.text_to_be_present_in_element((By.XPATH, "//div[@data-test-id='app-cart']"), context.product_title)
        )
        print("Item was successfully added to the cart")
    except TimeoutException:
        print("Timeout\n**")
    except Exception as e:
        print(e)
    context.driver.quit()


# 2nd test
@step('Click "Sign in" and and verify sign in page is opened')
def click_sign_in(context):
    context.sign_in_btn = context.driver.find_element(By.XPATH, "//span[@id='gh-ug']/a[text()='Sign in']")
    context.sign_in_btn.click()
    print("Clicked 'Sign in' button\n***")
    try:
        context.wait.until(
            ec.presence_of_element_located((By.XPATH, "//input[@id='userid']"), )
        )
        print("Sign in page has successfully opened\n***")
    except TimeoutException:
        print("Timeout\n**")
    except Exception as e:
        print(e)


@step('Click "register" and verify registration page has opened')
def click_register(context):
    context.register_btn = context.driver.find_element(By.XPATH, "//span[@id='gh-ug-flex']/a[text()='register']")
    context.register_btn.click()
    print("Clicked 'register' button\n***")
    try:
        context.wait.until(
            ec.presence_of_element_located((By.XPATH, "//button[@id='EMAIL_REG_FORM_SUBMIT']"))
        )
        print("Registration page has successfully opened\n***")
    except TimeoutException:
        print("Timeout\n**")
    except Exception as e:
        print(e)


@step('Click "Daily Deals" and verify daily deals page has opened')
def click_daily_deals(context):
    context.daily_deals_btn = context.driver.find_element(By.XPATH, "//a[text()=' Daily Deals' and @class='gh-p']")
    context.daily_deals_btn.click()
    print("Clicked 'Daily Deals' button\n***")
    expected_url = "https://www.ebay.com/deals"
    current_url = context.driver.current_url
    if current_url == expected_url:
        print("Daily Deals page has successfully opened\n***")
    else:
        print("Daily Deals page is not opened\n***")


@step('Click "Brand Outlet" and verify Brand Outlet page has opened')
def click_brand_outlet(context):
    context.brand_outlet_link = context.driver.find_element(By.XPATH, "//li[@id='gh-p-4']/a")
    context.brand_outlet_link.click()
    print("Clicked 'Brand Outlet' link\n***")
    try:
        context.wait.until(
            ec.presence_of_element_located((By.XPATH, "//a[@class='seo-breadcrumb-text']/span[text()='Brand Outlet']"))
        )
        print("Brand Outlet page has successfully opened\n***")
    except TimeoutException:
        print("Timeout\n**")
    except Exception as e:
        print(e)


@step('Click "Gift Cards" and verify gift cards page has opened')
def click_gift_cards(context):
    context.gift_cards_btn = context.driver.find_element(
        By.XPATH, "//a[contains(text(), 'Gift Cards') and @class='gh-p']"
    )
    context.gift_cards_btn.click()
    print("Clicked 'Gift Cards' button\n***")
    compare_urls(context.driver, "https://www.ebay.com/giftcards", "Gift Cards page")


@step('Click "Help & Contact" and verify help and contact page has opened')
def click_help(context):
    context.help_contact_btn = context.driver.find_element(
        By.XPATH, "//a[contains(text(),'Help & Contact') and @class='gh-p']"
    )
    context.help_contact_btn.click()
    print("Clicked 'Help & Contact' button\n***")
    wait_for_element_by_xpath(context.driver, "//a[@aria-current='location' and text()='Customer Service']")
    compare_urls(context.driver, "https://www.ebay.com/help/home", "Help & Contact page")


@step('Click "Sell" and verify sell page has opened')
def click_sell(context):
    context.sell_btn = context.driver.find_element(By.XPATH, "//a[contains(text(),'Sell') and @class='gh-p']")
    context.sell_btn.click()
    print("Clicked 'Sell' button\n***")
    compare_urls(context.driver, "https://www.ebay.com/sl/sell", "Sell page")


@step('Click {link} link')
def click_watchlist(context, link):
    context.watchlist_btn = context.driver.find_element(
        By.XPATH, f"//*[contains(@class,'gh-') and text() = '{link}']"
    )
    context.watchlist_btn.click()
    print("Clicked", link, "link\n***")


@step('Verify {dropdown_element} dropdown')
def verify_dropdown_element(context, dropdown_element):
    # WORK ON LINE 259, wait should be changed depending on dropdown
#    wait_for_element_by_xpath(context.driver, "//div[@class='rvi__title']")
    try:
        context.wait.until(
            ec.attribute_to_be(
                (By.XPATH, f"//*[contains(@class,'gh-') and text() = '{dropdown_element}']/following-sibling::a[@aria-expanded]"),
            "aria-expanded", "true"))
        print(dropdown_element, "has successfully opened\n***")
    except TimeoutException:
        print("Timeout\n**")
    except Exception as e:
        print(e)

    dropdown_exp = context.driver.find_element(
        By.XPATH, f"//*[contains(@class,'gh-') and text() = '{dropdown_element}']/following-sibling::a[@aria-expanded]"
    )
    aria_exp_value = dropdown_exp.get_attribute("aria-expanded")
    if aria_exp_value == "true":
        print(dropdown_element, "has been expanded\n***")
    else:
        print("\033[91m", dropdown_element, "has NOT expanded !\033[0m\n***")

#    check_dropdown(context.driver,f"//*[contains(@class,'gh-') and text() = '{dropdown_element}']/following-sibling::a[@aria-expanded]")
#    //*[contains(@class,'gh-') and text() = 'Watchlist']/following-sibling::a[@aria-expanded]
#    check_dropdown(context.driver, "//a[text()='Expand Watch List']", "Watch List dropdown")


@step('Hover over "My eBay" and verify my ebay dropdown menu has opened')
def hover_my_ebay(context):
    my_ebay_dd = context.driver.find_element(By.XPATH, "//a[@title='My eBay']")
    context.actions.move_to_element(my_ebay_dd).perform()
    print("Hovered over My eBay dropdown\n***")
    wait_for_element_by_xpath(context.driver, "//ul[@id='gh-ul-nav']/li/a[contains(text(),'Summary')]")
    check_dropdown(context.driver, "//a[text()='Expand My eBay']", "My eBay dropdown")


@step('Hover over notification icon and verify notifications have opened')
def hover_notification(context):
    context.notifications_icon = context.driver.find_element(By.XPATH, "//i[@id='gh-Alerts-i']//parent::button")
    context.actions.move_to_element(context.notifications_icon).perform()
    print("Hovered over notifications icon\n***")
    wait_for_element_by_xpath(context.driver, "//span[@class='ghn-errb ghn-errb-a']/a/span")
    check_dropdown(context.driver, "//i[@id='gh-Alerts-i']//parent::button", "Notifications")


@step('Click on cart icon and verify cart page has opened')
def verify_cart(context):
    cart_icon = context.driver.find_element(By.XPATH, "//li[@id='gh-minicart-hover']")
    cart_icon.click()
    print("Clicked on cart icon\n***")
    wait_for_element_by_xpath(context.driver, "//h1[@data-test-id='main-title' and text()='Shopping cart']")
    compare_urls(context.driver, "https://cart.ebay.com/", "Cart page")