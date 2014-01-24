from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class AddRemoveTable(object):
    """
    This class represents the table for adding/removing testcase from testplan
    """
    def __init__(self, browser, logger, by=By.TAG_NAME, value="table"):

        super(AddRemoveTable, self).__init__()
        self.browser = browser
        self.table = self.browser.find_element(by, value)
        self.logger = logger
        self.save_btn = self.browser.find_element(By.NAME, "doAddRemove")

    def get_case_grid(self, testcase):
        """
        Get the tooltip of the testcase
        """
        grids = self.table.find_elements(By.TAG_NAME, "td")

        for grid in grids:
            if testcase.case_id in grid.text:
                return grid
        raise TestcaseNotFoundError, ("Cannot find testcase: {t}"
                                      .format(t=testcase.case_id))

    def get_case_tooltip(self, testcase):
        """
        Get the tooltip of the given test case_id
        tooltip is for getting the checkbox of the testcase
        """
        grid = self.get_case_grid(testcase)
        tt = grid.get_attribute("id").replace("tooltip-", "")
        self.logger.info("Tooltip for case {c}: {t}"
                         .format(c=testcase.case_id, t=tt))
        return tt

    def get_platform_value(self, platform):
        """
        Get the value of the platform
        """
        if platform is None:
            return "0"
        else:
            select = self.browser.find_element(By.ID, "select_platform")
            options = select.find_elements(By.TAG_NAME, "option")

            for option in options:
                if platform.strip() == option.get_attribute("label").strip():
                    ret = option.get_attribute("value").strip()
                    self.logger.info("Value of platform {p}: {v}"
                                     .format(p=platform, v=ret))
                    return ret

            raise PlatformNotFoundError, ("The specified platform '{p}'"
                                          " cannot be cound".format(p=platform))

    def add_testcase_to_platform(self, testcase, platform):
        """
        Add testcase to platform
        """
        tooltip = self.get_case_tooltip(testcase)
        value = self.get_platform_value(platform)
        checkbox_name = "achecked_tc[{t}][{v}]".format(t=tooltip, v=value)

        try:
            self.table.find_element(By.NAME, checkbox_name).click()
            self.save_btn.click()
        except NoSuchElementException, err:
            self.logger.error("Can not find the check box for adding case: {c}"
                              .format(c=testcase.case_id))
            self.logger.error("It might caused by wrong case id or the case has"
                              " been added to the testplan or platform")
            self.logger.error("Name of checkbox: {n}".format(n=checkbox_name))

    def remove_testcase_to_platform(self, testcase, platform):
        """
        Add testcase to platform
        """
        tooltip = self.get_case_tooltip(testcase)
        value = self.get_platform_value(platform)
        checkbox_name = "remove_checked_tc[{t}][{v}]".format(t=tooltip, v=value)

        try:
            self.table.find_element(By.NAME, checkbox_name).click()
            self.save_btn.click()
        except NoSuchElementException, err:
            self.logger.error("Can not find the check box for removing "
                              "case: {c}".format(c=testcase.case_id))
            self.logger.error("It might caused by wrong case id or the case has"
                              " been removed from the testplan or platform")
            self.logger.error("Name of checkbox: {n}".format(n=checkbox_name))


class PlatformNotFoundError(Exception):
    pass


class TestcaseNotFoundError(Exception):
    pass
