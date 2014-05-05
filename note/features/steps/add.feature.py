# -*- coding: utf-8 -*-
from behave import given, when, then


@then(u'I should see link contents url "{content}"')
def i_should_see_link_contents_url(context, content):
    msg = context.browser.find_link_by_partial_href(content).first
    assert msg


@when(r'I visit url "{url}"')
def i_visit_url(context, url):
    br = context.browser
    br.visit(url)


@given(u'I am a visitor')
def i_am_a_visitor(context):
    pass


@then(u'I should see "{text}" somewhere in page')
def i_should_see_text_somwhere_in_page(context, text):
    assert text in context.browser.html


@when(u'I click link contents url "{text}"')
def i_click_link_contents_url_text(context, text):
    link = context.browser.find_link_by_partial_href(text).first
    assert link
    link.click()


@when(u'I click link contents "{text}"')
def i_click_link_contents_text(context, text):
    link = context.browser.find_link_by_partial_text(text).first
    assert link
    link.click()


@when(u'I input "{text}" in "{field}" field')
def i_input_text_in_field_field(context, text, field):
    field = context.browser.find_by_xpath("//label[contains(text(),'" + field + "')]/following-sibling::input").first
    assert field
    field.type(text, slowly=False)


@when(u'I click "{name}" button')
def i_click_name_button(context, name):
    button = context.browser.find_by_xpath("//button[contains(.,'" + name + "')]").first
    assert button
    button.click()


@when(u'I select "{value}" in "{name}" dropdown')
def i_select_value_in_name_dropdown(context, value, name):
    #dropdown = context.browser.find_by_xpath("//label[contains(text(),'" + name + "')]/following-sibling::select/option[@value='1']").first
    dropdown = context.browser.find_by_xpath(
        "//label[contains(text(),'" + name + "')]/following-sibling::select/option[text()='" + value + "']")
    assert dropdown
    dropdown.click()
