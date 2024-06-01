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
