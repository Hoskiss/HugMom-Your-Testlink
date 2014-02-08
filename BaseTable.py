import re
from selenium.webdriver.common.by import By


class BaseTable(object):

    """
    This class represents the base table
    table implemented for now:
        - UrgencyTable
        - AddRemoveTable
        - VersionTable
    """

    def __init__(self, browser, logger):

        self.browser = browser
        self.logger = logger
        self.table = None
        self.save_btn = None

    def _get_case_grid(self, case, by=By.TAG_NAME, value="td"):
        """
        return the grid which has the case id
        """
        grids = self.table.find_elements(by, value)

        for grid in grids:
            if case.case_id in grid.text:
                return grid
        raise TestcaseNotFoundError("Cannot find testcase: {t}"
                                    .format(t=case.case_id))

    def _get_case_row(self, case, by=By.TAG_NAME, value="tr"):
        """
        return the row which has the case id
        """
        rows = self.table.find_elements(by, value)

        for row in rows:
            if case.case_id in row.text:
                return row
        raise TestcaseNotFoundError("Cannot find testcase: {t}"
                                    .format(t=case.case_id))

    # Update Case Versions Table Can't use this way
    # def _get_case_tooltip(self, case):
    #     """
    #     Get the tooltip of the given test case_id
    #     tooltip is for getting the checkbox of the testcase
    #     """
    #     row = self._get_case_row(case)
    #     tt = row.get_attribute("id").replace("tooltip-", "")
    #     self.logger.debug("Tooltip for case {c}: {t}"
    #                      .format(c=case.case_id, t=tt))
    #     return tt

    def _get_case_tooltip(self, case):
        """
        Get the tooltip of the given test case_id
        tooltip is for getting the checkbox of the testcase
        """
        if hasattr(case, 'tooltip'):
            return case.tooltip

        elem = self.browser.wait_for_element(By.PARTIAL_LINK_TEXT,
                                             case.name)
        if elem is None:
            print "Can not find tooltip for case: {c}!".format(
                c=case.case_id)
            self.logger.debug("Can not find tooltip for case: {c}!"
                              .format(c=case.case_id))
            return None
        else:
            tooltip = elem.get_attribute("href")
            tooltip = re.search("\d+", tooltip).group()
            case.tooltip = tooltip
            self.logger.debug("Tooltip for case {c}: {t}"
                              .format(c=case.case_id, t=tooltip))
            return tooltip

    def _get_platform_value(self, platform):
        """
        Get the value of the platform
        """
        print "Deal with cases in {platform}".format(platform=platform)
        self.logger.info("Deal with cases in {platform}"
                         .format(platform=platform))

        if platform is None:
            return "0"
        else:
            select = self.browser.wait_for_element(By.ID, "select_platform")
            options = select.find_elements(By.TAG_NAME, "option")

            for option in options:
                if platform.strip() == option.get_attribute("label").strip():
                    ret = option.get_attribute("value").strip()
                    self.logger.info("Value of platform {p}: {v}"
                                     .format(p=platform, v=ret))
                    return ret

        raise PlatformNotFoundError("The specified platform '{p}'"
                                    " cannot be cound".format(p=platform))

    def save(self):
        """
        save the change
        """
        self.save_btn.click()


class PlatformNotFoundError(Exception):
    pass


class TestcaseNotFoundError(Exception):
    pass
