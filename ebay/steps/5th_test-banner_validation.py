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
    context.next_transitions = 0
    context.prev_transitions = 0


def get_active_slide_index(context):
    for i, slide in enumerate(context.banner_slides):
        if slide.get_attribute("aria-hidden") is None:
            return i
    return None


def check_slide_transition(context):
    # calculating indexes for next and previous slides
    expected_next_slide = (context.initial_slide_index + 1) % len(context.banner_slides)
    expected_prev_slide = (context.initial_slide_index - 1 + len(context.banner_slides)) % len(context.banner_slides)
    # getting the current active slide index
    new_active_slide_index = get_active_slide_index(context)
    # checking if transitioned to the next slide
    if new_active_slide_index == expected_next_slide:
        print(f"🛈 Transitioned to the next slide № {new_active_slide_index + 1}")
        context.initial_slide_index = new_active_slide_index  # update for next iteration
        context.next_transitions += 1
        return True
    # checking if transitioned to the previous slide
    elif new_active_slide_index == expected_prev_slide:
        print(f"🛈 Transitioned to the previous slide № {new_active_slide_index + 1}")
        context.initial_slide_index = new_active_slide_index  # update for next iteration
        context.prev_transitions += 1
        return True
    else:
        print("❌ Slide transition failed\n***")
        return False


def wait_for_slide_transition(context):
    # storing the current slide index before waiting for a change
    current_slide_index = context.initial_slide_index
    # waiting until the slide index changes from the current index
    context.wait.until(
        lambda driver: get_active_slide_index(context) != current_slide_index,
        message="Failed to transition to a different slide within the timeout period."
    )
    # getting the new active slide index after the transition
    new_slide_index = get_active_slide_index(context)
    # determining the direction of the transition and update context accordingly
    if new_slide_index == (current_slide_index + 1) % len(context.banner_slides):
        print(f"🛈 Transitioned to the next slide № {new_slide_index + 1}")
        context.next_transitions += 1
    elif new_slide_index == (current_slide_index - 1 + len(context.banner_slides)) % len(context.banner_slides):
        print(f"🛈 Transitioned to the previous slide № {new_slide_index + 1}")
        context.prev_transitions += 1
    else:
        print("❌ Slide transition failed or transitioned to a non-adjacent slide\n***")
    # updating the initial_slide_index for subsequent checks
    context.initial_slide_index = new_slide_index

# def wait_for_slide_transition(context):
#     context.wait.until(
#         lambda driver:
#         get_active_slide_index(context) == (context.initial_slide_index + 1) % len(context.banner_slides)
#     )


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
