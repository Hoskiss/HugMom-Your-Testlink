from selenium.webdriver.common.by import By

class UrgencyTable(object):
    """
    This class represents the table which set urgency of test cases
    """

    def __init__(self, browser, by=By.CLASS_NAME, value="simple_tableruler"):
        """
        """
        super(UrgencyTable, self).__init__()
        self.browser = browser
        self.table = self.browser.find_element(by, value)
        self.submit_btn = self.browser.find_element(
            By.CSS_SELECTOR,
            "input[value='Set urgency for individual testcases']")

    def get_case_row(self, case):
        """
        return the row which has the case id
        """
        rows = self.table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            if case.case_id in row.text:
                return TableRow(row)
        return None

    def submit(self):
        """
        submit the change
        """
        self.submit_btn.click()


class TableRow(object):
    """
    This class represents the row in the UrgencyTable
    """

    def __init__(self, element):
        self.element = element

    def set_urgency(self, urgency):
        """
        Set urgency in this row
        """
        urgency_map = {"High": u"3", "Medium": u"2", "Low": u"1"}
        radios = self.element.find_elements(By.TAG_NAME, "input")

        for radio in radios:
            if radio.get_attribute("value") == urgency_map[urgency]:
                radio.click()
                break
