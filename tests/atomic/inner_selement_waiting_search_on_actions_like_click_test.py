import pytest
from selenium.common.exceptions import TimeoutException

from tests.atomic.helpers.givenpage import GivenPage
from selenium import webdriver
from selene.tools import *

__author__ = 'yashaka'

driver = webdriver.Firefox()
GIVEN_PAGE = GivenPage(driver)
WHEN = GIVEN_PAGE
original_timeout = config.timeout
        
        
def setup_module(m):
    set_driver(driver)


def teardown_module(m):
    get_driver().quit()


def setup_function(fn):
    global original_timeout


def test_waits_for_inner_visibility():
    GIVEN_PAGE\
        .opened_with_body(
            '''
            <p>
                <a href="#second" style="display:none">go to Heading 2</a>
                <h2 id="second">Heading 2</h2>
            </p>''')\
        .execute_script_with_timeout(
            'document.getElementsByTagName("a")[0].style = "display:block";',
            250)

    s('p').find('a').click()
    assert ('second' in get_driver().current_url) is True


def test_waits_for_inner_presence_in_dom_and_visibility():
    GIVEN_PAGE.opened_with_body(
            '''
            <p>
                 <h2 id="second">Heading 2</h2>
            </p>''')
    WHEN.load_body_with_timeout(
            '''
            <p>
                <a href="#second">go to Heading 2</a>
                <h2 id="second">Heading 2</h2>
            </p>''',
            250)

    s('p').find('a').click()
    assert ('second' in get_driver().current_url) is True


def test_waits_first_for_inner_presence_in_dom_then_visibility():
    GIVEN_PAGE.opened_with_body(
            '''
            <p>
                <h2 id="second">Heading 2</h2>
            </p>''')
    WHEN.load_body_with_timeout(
            '''
            <p>
                <a href="#second" style="display:none">go to Heading 2</a>
                <h2 id="second">Heading 2</h2>
            </p>''',
            250)\
        .execute_script_with_timeout(
            'document.getElementsByTagName("a")[0].style = "display:block";',
            500)

    s('p').find('a').click()
    assert ('second' in get_driver().current_url) is True


def test_waits_first_for_parent_in_dom_then_inner_in_dom_then_visibility():
    GIVEN_PAGE.opened_empty()
    WHEN.load_body_with_timeout(
            '''
            <p>
                <h2 id="second">Heading 2</h2>
            </p>''',
            250)
    WHEN.load_body_with_timeout(
            '''
            <p>
                <a href="#second" style="display:none">go to Heading 2</a>
                <h2 id="second">Heading 2</h2>
            </p>''',
            500)\
        .execute_script_with_timeout(
            'document.getElementsByTagName("a")[0].style = "display:block";',
            750)

    s('p').find('a').click()
    assert ('second' in get_driver().current_url) is True


# todo: there should be each such test method for each "passing" test from above...
def test_fails_on_timeout_during_waiting_for_inner_visibility():
    config.timeout = 0.25
    GIVEN_PAGE\
        .opened_with_body(
            '''
            <p>
                <a href='#second' style='display:none'>go to Heading 2</a>
                <h2 id='second'>Heading 2</h2>
            </p>''')\
        .execute_script_with_timeout(
            'document.getElementsByTagName("a")[0].style = "display:block";',
            500)

    with pytest.raises(TimeoutException):
        s('p').find('a').click()
    assert ('second' in get_driver().current_url) is False

