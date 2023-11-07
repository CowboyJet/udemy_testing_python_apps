from behave import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from video_code.tests.acceptance.locators.blog_page import BlogPageLocators

@given("I wait for the posts to load")
def step_impl(context):
    WebDriverWait(context.driver, 5).until(
        expected_conditions.visibility_of_element_located(BlogPageLocators.POSTS_SECTION)
    )