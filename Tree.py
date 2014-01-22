from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tree(object):
    """
    This class represents the tree view in the testlink ui
    """
    def __init__(self, browser, logger):
        """
        """
        super(Tree, self).__init__()
        self.browser = browser
        self.logger = logger
        self.collapse_btn = self.browser.find_element(By.NAME, "collapse_tree")

    def get_tree_nodes(self):
        return [TreeNode(e) for e in
                self.browser.find_elements(By.CLASS_NAME, "x-tree-node-el")]

    def expand_folder(self, folder_name):
        """
        find and click on the icon to expand the folder
        """
        nodes = self.get_tree_nodes()

        # expand the test suite of the case
        flag = False
        for node in nodes:
            if node.text.startswith(folder_name):
                self.logger.info("Expand suite: " + folder_name)
                node.expand()
                flag = True

        if not flag:
            raise FolderNotFoundError, "CAN NOT FIND FOLDER: " + folder_name

    def click_folder(self, folder_name):
        """
        find and click on the icon to expand the folder
        """
        nodes = self.get_tree_nodes()

        # expand the test suite of the case
        flag = False
        for node in nodes:
            if node.text.startswith(folder_name):
                self.logger.info("Click suite: " + folder_name)
                node.click()
                flag = True

        if not flag:
            raise FolderNotFoundError, "CAN NOT FIND FOLDER: " + folder_name

    def expand_case(self, case):
        """
        expand the test case
        """
        self.expand_folder(case.test_suite)

        # expand the sub folder in the sub path, besides the last one
        # because we dont need to expand it
        for folder_name in case.sub_path[:-1]:
            self.expand_folder(folder_name)

        # click on the last folder of the case
        self.click_folder(case.sub_path[-1])

    def collapse_all_node(self):
        """
        collapse the tree by clicking on the button
        """
        self.collapse_btn.click()

    def wait_for_present(self, timeout=60):
        """
        wait for tree area to present in the browser
        """
        wait = WebDriverWait(self.browser, timeout)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                   "x-tree-ec-icon")))

class TreeNode(object):
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
        self.element.find_element(By.CLASS_NAME, "x-tree-ec-icon").click()

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