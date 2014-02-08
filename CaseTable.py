import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from BaseTable import BaseTable


class AddRemoveTable(BaseTable):

    """
    This class represents the table for adding/removing testcase from testplan
    """

    def __init__(self, browser, logger):

        super(AddRemoveTable, self).__init__(browser, logger)
        self.table = self.browser.find_element(By.TAG_NAME, "table")
        self.save_btn = self.browser.find_element(By.NAME, "doAddRemove")

    def move_case_for_platform(self, action, case, platform):
        """
        Add/Remove testcase for platform
        """
        tooltip = self._get_case_tooltip(case)
        value = self._get_platform_value(platform)

        if "add" == action:
            checkbox_name = "achecked_tc[{t}][{v}]".format(t=tooltip, v=value)
        elif "remove" == action:
            checkbox_name = "remove_checked_tc[{t}][{v}]".format(
                t=tooltip, v=value)
        else:
            print "{act} case does not support!".format(act=action)
            self.logger.error(
                "{act} case does not support!".format(act=action))

        try:
            self.table.find_element(By.NAME, checkbox_name).click()
            self.save()
            time.sleep(1)

            print "{act} < {full_name} > for {platform}!".format(
                act=action, full_name=case.full_name, platform=platform)
            self.logger.info("{act} < {full_name} > for {platform}!".format(
                act=action, full_name=case.full_name, platform=platform))

        except NoSuchElementException as err:
            print "Can not find the check box for {act} case: {c}".format(
                act=action, c=case.case_id)
            self.logger.error("Can not find the check box for {act} case: {c}"
                              .format(act=action, c=case.case_id))
            self.logger.error("It might caused by wrong case id or the case "
                              "has been added to the testplan or platform")
            self.logger.error("Name of checkbox: {n}".format(n=checkbox_name))


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

        grid = self._get_case_grid(case)
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
            time.sleep(1)
            print "Assign < {full_name} > to {tester} !".format(
                full_name=case.full_name, tester=tester)
            self.logger.info("Assign < {full_name} > to {tester} !".format(
                full_name=case.full_name, tester=tester))
        except:
            print "check your tester: {tester} if exists!".format(
                tester=tester)
            self.logger.debug("check your tester: {tester} if exists!".format(
                tester=tester))


class UrgencyTable(BaseTable):

    """
    This class represents the table which set urgency of test cases
    """

    def __init__(self, browser, logger):
        """
        """
        super(UrgencyTable, self).__init__(browser, logger)
        self.table = self.browser.find_element(
            By.CLASS_NAME, "simple_tableruler")
        self.save_btn = self.browser.find_element(
            By.CSS_SELECTOR,
            "input[value='Set urgency for individual testcases']")
        self.URGENCY_MAP = {"High": u"3", "Medium": u"2", "Low": u"1"}

    def set_case_urgency(self, case, urgency):
        case_row = self._get_case_row(case)
        radios = case_row.find_elements(By.TAG_NAME, "input")
        for radio in radios:
            if radio.get_attribute("value") == self.URGENCY_MAP[urgency]:
                radio.click()
                print "set < {full_n} > urgency to {urcy} !".format(
                    full_n=case.full_name, urcy=urgency)
                self.logger.info("set < {full_n} > urgency to {urcy} !".format(
                    full_n=case.full_name, urcy=urgency))
                break

        self.save()
        time.sleep(1)
        print "set {p_key} urgency!".format(p_key=urgency)
        self.logger.info("set {p_key} urgency!".format(p_key=urgency))


class VersionTable(BaseTable):

    """
    This class represents the table which update version of test cases
    """

    def __init__(self, browser, logger):
        """
        """
        super(VersionTable, self).__init__(browser, logger)
        self.table = self.browser.find_element(By.TAG_NAME, "table")
        self.save_btn = self.browser.find_element(By.ID, "update_btn")

    def update_case_version(self, case):
        tooltip = self._get_case_tooltip(case)
        if tooltip is None:
            print ("update case failed, check if < {full_n} > "
                   "in the test plan!".format(full_n=case.full_name))
            self.logger.error("update case failed, check if < {full_n} > in "
                              "the test plan!".format(full_n=case.full_name))
            return

        update_checkbox_id = "achecked_tc{count}".format(
            count=tooltip)
        self.browser.find_element(By.ID, update_checkbox_id).click()

        self.save()
        time.sleep(1)
        print "update < {full_n} > !".format(full_n=case.full_name)
        self.logger.info("update < {full_n} > !".format(full_n=case.full_name))

    def update_folder_version(self, folder_path):
        self.browser.find_element(By.CSS_SELECTOR,
                                  "div.workBack h3.testlink img").click()
        self.save()
        time.sleep(1)
        print "update folder < {f_path} > !".format(
            f_path="||".join(folder_path))
        self.logger.info("update folder < {f_path} > !"
                         .format(f_path="||".join(folder_path)))
