import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class CaseTree(object):

    """
    This class represents the tree view in the testlink ui
    """

    def __init__(self, browser, logger):
        """
        """
        self.browser = browser
        self.logger = logger
        self.collapse_btn = self.browser.wait_for_element(
            By.NAME, "collapse_tree")
        self.suite_collect = Select(self.browser.wait_for_element(
            By.NAME, "filter_toplevel_testsuite"))

    def _wait_for_present(self, timeout=20):
        """
        wait for tree area to present in the browser
        """
        self.browser.wait_for_element(By.CLASS_NAME, "x-tree-ec-icon",
                                      timeout)

    def get_nodes(self):
        return [CaseTreeNode(elem) for elem in
                self.browser.find_elements(By.CLASS_NAME, "x-tree-node-el")]

    def get_folder_node(self, folder_name):
        """
        Get the node object by given folder name
        """
        nodes = self.get_nodes()
        # the first one is always root Splunk folder
        for node in nodes[1:]:
            try:
                node_name = re.search(r"(?P<n>[^\(]*)\(", node.text).group("n")
            # some node are case name (after folder), not folder name
            except:
                continue
            if node_name.strip() == folder_name:
                self.logger.info("Got node: " + folder_name)
                return node

        raise FolderNotFoundError("CAN NOT FIND FOLDER: " + folder_name)

    def expand_folder(self, folder_name):
        """
        find and click on the icon to expand the folder
        """
        self.get_folder_node(folder_name).expand()

    def click_folder(self, folder_name):
        """
        find and click on the icon to expand the folder
        """
        self.get_folder_node(folder_name).click()

    def expand_case(self, case):
        """
        expand the test case
        """
        self._wait_for_present()
        self.expand_folder(case.test_suite)
        time.sleep(0.5)
        # expand the sub folder in the sub path, besides the last one
        # because we dont need to expand it
        for folder_name in case.sub_path[:-1]:
            self.expand_folder(folder_name)
            time.sleep(0.5)
        # click on the last folder of the case
        self.click_folder(case.sub_path[-1])
        time.sleep(0.5)

    def expand_folder_path(self, folder_path):
        """
        expand the test folder path
        """
        self._wait_for_present()
        # expand the sub folder in the folder_path, besides the last one
        # because we dont need to expand it
        for folder_name in folder_path[:-1]:
            self.expand_folder(folder_name)
            time.sleep(0.5)
        # click on the last folder of the case
        self.click_folder(folder_path[-1])
        time.sleep(0.5)

    def collapse_all_node(self):
        """
        collapse the tree by clicking on the button
        """
        self.collapse_btn.click()
        time.sleep(1)

    def select_test_suite(self, test_suite):
        self.suite_collect.select_by_visible_text(
            "{suite}".format(suite=test_suite))
        self.browser.find_element(
            By.CSS_SELECTOR, "input#doUpdateTree").click()
        time.sleep(2)


class CaseTreeNode(object):

    """
    This class represents the tree node in testlink ui
    """

    def __init__(self, element):
        """
        Constructor
        """
        self.element = element

    def expand(self):
        """
        expand the node
        """
        icon = self.element.find_element(By.CLASS_NAME, "x-tree-ec-icon")
        if ("x-tree-elbow-plus" in icon.get_attribute("class") or
            "x-tree-elbow-end-plus" in icon.get_attribute("class")):
            icon.click()

    def click(self):
        """
        Click on the node
        """
        self.element.find_element(By.CLASS_NAME, "x-tree-node-anchor").click()

    @property
    def text(self):
        return self.element.text


class FolderNotFoundError(Exception):
    pass
