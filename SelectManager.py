import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class KeywordManager():

    """
    This class represents the table for adding/removing keyword to/of case
    """

    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.save_btn = self.browser.wait_for_element(
            By.NAME, "assigntestcase")
        self.mouse = ActionChains(self.browser)

    def add_keyword_to_case(self, case, keyword):
        """
        Add keyword for case
        """
        try:
            # need select first!
            select_elem = self.browser.wait_for_element(
                By.CSS_SELECTOR,
                "#from_select_box".format(key=keyword))
            Select(select_elem).select_by_visible_text(keyword)

            elem = select_elem.find_element(
                By.CSS_SELECTOR,
                "option[label={key}]".format(key=keyword))
            self.mouse.double_click(elem).perform()

            self.save_btn.click()
            print "add keyword < {key} > for {c}!".format(key=keyword,
                                                          c=case.case_id)
            self.logger.info("add keyword < {key} > for {c}!".format(
                key=keyword, c=case.case_id))

        except:
            print "Can not add keyword for case: {c}!".format(
                c=case.case_id)
            self.logger.debug("Can not add keyword for case: {c}!"
                              .format(c=case.case_id))
