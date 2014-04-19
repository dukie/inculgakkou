from splinter.browser import Browser
from incul import test_populate
from selenium import webdriver


def before_all(context):
    context.browser = Browser(driver_name='firefox')



def after_all(context):
    context.browser.quit()
    context.browser = None
