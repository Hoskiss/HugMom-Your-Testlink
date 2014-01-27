from selenium.webdriver.common.by import By
from BaseTable import BaseTable
import time


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
        update_checkbox_id = "achecked_tc{count}".format(
            count=tooltip)
        self.browser.find_element(By.ID, update_checkbox_id).click()

        self.save()
        time.sleep(2)
        print "update < {full_n} > !".format(full_n=case.full_name)
        self.logger.info("update < {full_n} > !".format(full_n=case.full_name))

    def update_folder_version(self, folder_path):
        self.browser.find_element(By.CSS_SELECTOR,
                                  "div.workBack h3.testlink img").click()
        self.save()
        time.sleep(2)
        print "update folder < {f_path} > !".format(
            f_path="||".join(folder_path))
        self.logger.info("update folder < {f_path} > !"
                         .format(f_path="||".join(folder_path)))
