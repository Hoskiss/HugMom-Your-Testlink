from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from BaseTable import BaseTable
import time
import re


class AssignTable(BaseTable):

    """
    This class represents the table which assign test cases to tester
    """

    def __init__(self, browser, logger):
        """
        """
        super(AssignTable, self).__init__(browser, logger)
        self.table = self.browser.find_element(By.TAG_NAME, "table")
        self.save_btn = self.browser.find_element(By.NAME, "doAction")

    def _get_case_tooltip(self, case):
        if hasattr(case, 'tooltip'):
            return case.tooltip

        grid = self.get_case_grid(case)

        try:
            #row = grid.find_element(By.XPATH, "..")
            row = grid.find_element(By.XPATH, "parent::tr")

            checkbox = row.find_element(
                By.CSS_SELECTOR, "input[type='checkbox']")
            tooltip = checkbox.get_attribute("name")
            tooltip = re.search("\[(?P<tt>\d+)\]", tooltip).group("tt")
            case.tooltip = tooltip
            self.logger.debug("Tooltip for case {c}: {t}"
                              .format(c=case.case_id, t=tooltip))
            return tooltip

        except:
            print "Can not find tooltip for case: {c}!".format(
                c=case.case_id)
            self.logger.debug("Can not find tooltip for case: {c}!"
                              .format(c=case.case_id))

    def assign_case_to_tester(self, case, tester, platform):
        tooltip = self._get_case_tooltip(case)
        p_value = self._get_platform_value(platform)

        try:
            elem = self.browser.wait_for_element(
                By.NAME, "tester_for_tcid[{tt}][{p_v}]".format(
                tt=tooltip, p_v=p_value))
        except:
            print "check your {platf} for {c} if exists!".format(
                platf=platform, c=case.full_name)
            self.logger.debug("check your {platf} for {c} if exists!".format(
                platf=platform, c=case.full_name))

        try:
            Select(elem).select_by_visible_text(tester)
            self.save()
            print "Assign < {full_name} > to {tester} !".format(
                full_name=case.full_name, tester=tester)
            self.logger.info("Assign < {full_name} > to {tester} !".format(
                full_name=case.full_name, tester=tester))
        except:
            print "check your tester: {tester} if exists!".format(
                tester=tester)
            self.logger.debug("check your tester: {tester} if exists!".format(
                tester=tester))
