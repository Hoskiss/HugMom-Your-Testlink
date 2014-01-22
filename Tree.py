from selenium.webdriver.common.by import By


class Tree(object):
    """
    This class represents the tree view in the testlink ui
    """
    def __init__(self, browser):
        """
        """
        super(Tree, self).__init__()
        self.browser = browser

    def get_tree_nodes(self):
        return [TreeNode(e) for e in
                self.browser.find_elements(By.CLASS_NAME, "x-tree-node-el")]

    def expand_case(self, case):
        """
        expand the test case
        """
        nodes = self.get_tree_nodes()

        # expand the test suite of the case
        for node in nodes:
            if case.test_suite in node.text:
                node.expand()

        # expand the sub folder in the sub path, besides the last one
        # because we dont need to expand it
        for folder_name in case.sub_path[:-1]:
            nodes = self.get_tree_nodes()
            for node in nodes:
                if folder_name in node.text:
                    node.expand()

        # click on the last folder of the case
        nodes = self.get_tree_nodes()
        for node in nodes:
            if case.sub_path[-1] in node.text:
                node.click()


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
