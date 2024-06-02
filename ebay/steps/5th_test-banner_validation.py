###
# 5TH TEST - BANNER VALIDATION

from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


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
    print("✅ Banner is spinning\n***")


@step('Validate {number_of_spins} banner transitions')
def banner_spin_validation(context, number_of_spins):
    for _ in range(int(number_of_spins)-1):  # -1 due to initial successful transition from previous step
        try:
            wait_and_check_transition(context)
        except Exception as e:
            print("\033[91m ❌ An error occurred:\033[0m", e, "\n***")
    print(f"✅ Banner has successfully made {context.successful_transitions} transitions\n***")
