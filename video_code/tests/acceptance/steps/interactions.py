from behave import *

from video_code.tests.acceptance.page_model.base_page import BasePage
from video_code.tests.acceptance.page_model.new_post_page import NewPostPage

@when('I click on the "{link_text}" link')
def step_impl(context, link_text):
    page = BasePage(context.driver)
    links = page.navigation

    matching_links = [l for l in links if l.text == link_text]

    if matching_links:
        matching_links[0].click()
    else:
        raise RuntimeError

@when('I enter "{content}" in the "{field_name}" field')
def step_impl(context, content, field_name):
    page = NewPostPage(context.driver)
    page.form_field(field_name).send_keys(content)


@when("I press the submit button")
def step_impl(context):
    page = NewPostPage(context.driver)
    page.submit_button.click()
