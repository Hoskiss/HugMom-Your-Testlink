from selenium.webdriver.common.by import By
#from selenium.common.exceptions import NoSuchElementException
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

        if "add"==action:
            checkbox_name = "achecked_tc[{t}][{v}]".format(t=tooltip, v=value)
        elif "remove"==action:
            checkbox_name = "remove_checked_tc[{t}][{v}]".format(t=tooltip, v=value)
        else:
            print "{act} case does not support!".format(act=action)
            self.logger.error("{act} case does not support!".format(act=action))

        try:
            self.table.find_element(By.NAME, checkbox_name).click()
            self.save_btn.click()

            print "{act} < {full_name} > for {platform}!".format(
                act=action, full_name=case.full_name, platform=platform)
            self.logger.info("{act} < {full_name} > for {platform}!".format(
                act=action, full_name=case.full_name, platform=platform))

        except NoSuchElementException, err:
            print "Can not find the check box for {act} case: {c}".format(
                act=action, c=case.case_id)
            self.logger.error("Can not find the check box for {act} case: {c}"
                              .format(act=action, c=case.case_id))
            self.logger.error("It might caused by wrong case id or the case has"
                              " been added to the testplan or platform")
            self.logger.error("Name of checkbox: {n}".format(n=checkbox_name))

