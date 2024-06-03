
# 5TH TEST - BANNER VALIDATION

from behave import step
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from time import sleep


@step('Make sure the banner is visible')
def banner_visibility(context):
    context.wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "//div[@aria-roledescription='Carousel'][.//div[@class='tracking-wrapper']]")),
        message="❌ Banner isn't visible\n***"
    )
    print("✅ Banner is visible\n***")
    # collecting banner slides
    context.banner_slides = context.driver.find_elements(
        By.XPATH, "//li[@class='carousel__snap-point vl-carousel__item'][div[@class='tracking-wrapper']]")
    # initializing counts and indexes
    context.successful_transitions = 0
    context.initial_slide_index = get_active_slide_index(context)


def get_active_slide_index(context):
    for i, slide in enumerate(context.banner_slides):
        if slide.get_attribute("aria-hidden") is None:
            return i
    return None


def check_slide_transition(context, new_slide_index):
    current_slide_index = context.initial_slide_index
    if new_slide_index == (current_slide_index + 1) % len(context.banner_slides):
        print(f"🛈 Transitioned to the next slide № {new_slide_index + 1}")
        context.successful_transitions += 1
    elif new_slide_index == (current_slide_index - 1 + len(context.banner_slides)) % len(context.banner_slides):
        print(f"🛈 Transitioned to the previous slide № {new_slide_index + 1}")
        context.successful_transitions += 1
    else:
        print("❌ Slide transition failed\n***")
    context.initial_slide_index = new_slide_index  # updating the index for next iteration


def wait_and_check_transition(context):
    # waiting for slide transition
    context.wait.until(
        lambda driver: get_active_slide_index(context) != context.initial_slide_index,
        message="❌ Timeout: Failed to make a transition"
    )
    new_slide_index = get_active_slide_index(context)
    check_slide_transition(context, new_slide_index)


@step('Validate the banner is spinning by default')
def auto_banner_spin(context):
    print(f"🛈 Initial slide № {context.initial_slide_index + 1} is visible")
    try:
        wait_and_check_transition(context)
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
    print("✅ Carousel is spinning by default\n***")


@step('Validate {number_of_spins} banner transitions')
def banner_spin_validation(context, number_of_spins):
    print(f"🛈 Validating {number_of_spins} more transitions..")
    for _ in range(int(number_of_spins)):  # -1 due to initial successful transition from previous step
        try:
            wait_and_check_transition(context)
        except Exception as e:
            print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
    print(f"✅ Banner has successfully made {number_of_spins} more transitions\n***")


@step('Verify pause button is working and it pauses automatic slide scrolling')
def pause_button_validation(context):
    pause_btn = context.driver.find_element(By.XPATH, "//button[@aria-label='Pause Banner Carousel']")
    pause_btn.click()
    # context.driver.execute_script("arguments[0].click();", pause_btn)  # try js click in case transitions are breaking
    print("🛈 Clicked the pause button\n🛈 Waiting for a couple of seconds to verify that the carousel is paused..")
    # initializing local WebDriverWait with a specific timeout
    from selenium.webdriver.support.wait import WebDriverWait
    wait = WebDriverWait(context.driver, 6)
    initial_slide_index = get_active_slide_index(context)
    # verifying that the carousel is paused
    try:
        wait.until_not(
            lambda driver: get_active_slide_index(context) == initial_slide_index
        )
        print("❌ Pausing didn't work\n***")
    except TimeoutException:
        # if the exception is raised, it means the slide did not change within the timeout, indicating success
        print("✅ Carousel has been successfully paused\n***")


@step('Verify resume button is working and it resumes automatic slide scrolling')
def resume_button_validation(context):
    try:
        resume_btn = context.driver.find_element(By.XPATH, "//button[@aria-label='Play Banner Carousel']")
        resume_btn.click()
        # context.driver.execute_script("arguments[0].click();", resume_btn)
        print("🛈 Clicked the resume button")
        wait_and_check_transition(context)
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
    # initializing local WebDriverWait with a specific timeout
    from selenium.webdriver.support.wait import WebDriverWait
    wait = WebDriverWait(context.driver, 6)
    initial_slide_index = get_active_slide_index(context)
    # waiting until the slide index changes, indicating a successful transition
    try:
        wait.until(
            lambda driver: get_active_slide_index(context) != initial_slide_index
        )
        new_slide_index = get_active_slide_index(context)
        print(f"✅ Carousel is resumed and automatically moved to slide № {new_slide_index + 1}\n***")
    except TimeoutException:
        print("❌ Carousel didn't resume automatic sliding as expected\n***")


@step('Verify forward button is working and switching to the next slide')
def forward_button_switching(context):
    try:
        sleep(1)
        forward_btn = context.driver.find_element(By.XPATH, "//button[@aria-label='Go to next banner']")
        forward_btn.click()
        # context.driver.execute_script("arguments[0].click();", forward_btn)
        print("🛈 Clicked the forward button")
        wait_and_check_transition(context)
        print("✅ Forward button is working\n***")
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")


@step('Verify previous button is working and switching to the previous slide')
def previous_button_switching(context):
    try:
        sleep(1)  # using implicit wait due to carousel transition animations
        backward_btn = context.driver.find_element(By.XPATH, "//button[@aria-label='Go to previous banner']")
        backward_btn.click()
        # context.driver.execute_script("arguments[0].click();", backward_btn)
        print("🛈 Clicked the backward button")
        wait_and_check_transition(context)
        print("✅ Backward button is working\n***")
    except Exception as e:
        print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
