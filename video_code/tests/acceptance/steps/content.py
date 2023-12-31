from behave import *
from video_code.tests.acceptance.page_model.base_page import BasePage
from video_code.tests.acceptance.page_model.blog_page import BlogPage


@then("There is a title shown on the page")
def step_impl(context):
    page = BasePage(context.driver)
    assert page.title.is_displayed()


@then('The title tag has content "{content}"')
def step_impl(context, content):
    page = BasePage(context.driver)
    assert page.title.text == content


@then('I can see there is a posts section on the page')
def step_impl(context):
    page = BlogPage(context.driver)

    assert page.posts_section.is_displayed()


@then('I can see there is a post with title "{title}" in the posts section')
def step_impl(context, title):
    page = BlogPage(context.driver)
    posts_with_title = [p for p in page.posts if p.text == title]

    assert len(posts_with_title) > 0
    assert all([p.is_displayed() for p in posts_with_title])
