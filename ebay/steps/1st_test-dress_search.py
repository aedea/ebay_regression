###
# 1ST TEST - DRESS SEARCH

from behave import step
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


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
