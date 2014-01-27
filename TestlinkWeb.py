from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException

import time
import os
import logging
import re
import string
from Tree import Tree, FolderNotFoundError
from UrgencyTable import UrgencyTable
from AddRemoveTable import *
from VersionTable import VersionTable
from AssignTable import AssignTable

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import types

class TestlinkCase(object):

    def __init__(self, case_id):
        self.case_id = case_id
        file_name = os.path.basename(__file__).split(".")[0]
        self.logger = logging.getLogger(file_name)

    def print_id(self):
        print "Deal with {my_id}:".format(my_id=self.case_id)
        self.logger.info("Deal with {my_id}:".format(my_id=self.case_id))


# Add wait method for TestlinkWeb.browser
def wait_for_element(self, by, value, timeout=20):
    """
    wait for element to present in the browser
    """
    wait = WebDriverWait(self, timeout)
    wait.until(EC.presence_of_element_located((by, value)))
    return self.find_element(by, value)

class TestlinkWeb(object):

    """
    Version: 0.5 / 2014.01.27
        - set case priority
        - set case urgency
        - add/remove case for testplan
        - update case version in testplan
        - assign case of one platform to tester in testplan
    """

    def __init__(self, browser=None):
        self.URL = "http://testlink.splunk.com/index.php"
        self.PRIORITY_MAP = {"High": "3",
                             "Medium": "2",
                             "Low": "1"}
        self.browser = browser or webdriver.Firefox()
        self.browser.wait_for_element = types.MethodType(wait_for_element,
                                                         self.browser)

        # logging
        file_name = os.path.basename(__file__).split(".")[0]
        logger = logging.getLogger(file_name)
        logger.setLevel(logging.DEBUG)

        # create a file handler
        handler = logging.FileHandler(file_name + '.log', mode='w')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(handler)
        self.logger = logger

    def __del__(self):
        """
        Destructor
        """
        #self.browser.close()

    def open(self):
        """
        Open testlink homepage
        """
        self.browser.get(self.URL)

    def login(self, login_user, login_pwd):
        self.open()
        self.browser.find_element(By.ID, "login").send_keys(login_user)
        self.browser.find_element(By.NAME, "tl_password").send_keys(
            login_pwd + Keys.RETURN)
        time.sleep(2)
        try:
            # login failed
            self.browser.find_element(By.ID, "login")
            print ("your login name/password seems invalid, "
                   "please check and input again")
            return False
        except:
            return True

    def _open_case(self, case):
        self.open()
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("titlebar")
        input_id = self.browser.find_element(By.NAME, "targetTestCase")
        input_id.clear()
        input_id.send_keys("splunk-" + case.case_id + Keys.RETURN)
        time.sleep(2)

    def _get_case_path(self, case):
        self._open_case(case)
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")

        get_path = self.browser.find_element(
            By.CSS_SELECTOR, "div.workBack h2").text
        self.logger.debug("get_path: " + get_path)
        # path rule: first part is global "splunk"
        #           second part is test suite, ex: "UI"
        #           last one is case name
        case.test_suite = get_path.split("/")[1].strip()
        case.full_name = re.search("/ (?P<f_name>splunk-\d+:.+)",
                                   get_path).group('f_name').strip()
        case.name = re.search("^splunk-\d+:(?P<name>.+)",
                              case.full_name).group('name').strip()
        case.sub_path = map(
            string.strip,
            get_path.replace("/ " + case.full_name, "").split(" / "))
        case.sub_path = case.sub_path[2:]

        self.logger.debug("*" * 15)
        self.logger.debug("case.case_id: " + case.case_id)
        self.logger.debug("case.test_suite: " + case.test_suite)
        self.logger.debug("case.full_name: " + case.full_name)
        self.logger.debug("case.name: " + case.name)
        self.logger.debug("case.sub_path: " + str(case.sub_path))
        self.logger.debug("*" * 15)

    def select_test_plan(self, which_plan="6.0.2"):
        self.open()
        time.sleep(2)

        # select test project
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("titlebar")
        Select(self.browser.find_element(
            By.NAME, "testproject")).select_by_visible_text("Splunk")
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        Select(self.browser.find_element(
            By.NAME,"testplan")).select_by_visible_text(
            "{which_plan} Test Plan".format(which_plan=which_plan))
        time.sleep(2)
        print "Deal with cases in {plan}".format(plan=which_plan)
        self.logger.info("Deal with cases in {plan}"
                         .format(plan=which_plan))

    def switch_to_workframe(self):
        """
        """
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        self.browser.switch_to_frame("workframe")

    def switch_to_treeframe(self):
        """
        """
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        self.browser.switch_to_frame("treeframe")

    def set_case_priority(self, case, priority="High"):
        case.print_id()
        self._open_case(case)

        #self.browser.switch_to_frame(self.browser.find_elements(By.XPATH, "//frame")[0])
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")

        # case can be edited
        try:
            self.browser.find_element(By.NAME, "edit_tc").click()
            time.sleep(2)
        except:
            # need create new version
            try:
                self.browser.wait_for_element(
                    By.NAME, "do_create_new_version").click()
                self.browser.wait_for_element(
                    By.NAME, "edit_tc").click()

                time.sleep(2)
            # can not edit case, possibly case does not exist
            except:
                print "Case may not be exist, please check!"
                self.logger.info("Case may not be exist, please check!")
                return

        priority_select = Select(
            self.browser.find_element(By.NAME, "importance"))

        if priority != priority_select.first_selected_option.text:
            priority_select.select_by_value(self.PRIORITY_MAP[priority])
            self.browser.find_element(
                By.CSS_SELECTOR, "input[type='submit']").click()
            time.sleep(2)
            print "set {p_key} priority!".format(p_key=priority)
            self.logger.info("set {p_key} priority!".format(p_key=priority))

        else:
            print "** is already {p_key}!".format(p_key=priority)
            self.logger.info("** is already {p_key}!".format(p_key=priority))

    def set_case_urgency(self, test_plan, urgency, case):
        """
        Set the urgency of the tese case
        """
        case.print_id()
        self._get_case_path(case)

        self.select_test_plan(test_plan)
        self.browser.find_element(
            By.LINK_TEXT, "Set Urgent Tests").click()

        try:
            # expand the case
            self.logger.info("expand " + case.case_id)
            self.switch_to_treeframe()
            tree = Tree(self.browser, self.logger)
            tree.wait_for_present()
            tree.expand_case(case)
        except FolderNotFoundError as error:
            self.logger.error("Error while finding the case: {c} in the tree"
                              .format(c=case.case_id))
            self.logger.error(error)
            return None
        except TimeoutException as error:
            self.logger.error("Time out waiting for tree view to present")
            return None

        # set urgency of the case
        self.switch_to_workframe()
        table = UrgencyTable(self.browser)
        row = table.get_case_row(case)
        row.set_urgency(urgency)
        table.submit()

    def move_case(self, case, action, test_plan, platform):
        """
        Add or remove test case from the plan at the platform
        """
        if "add" != action and "remove" != action:
            print "check your second parameter, should be 'add' or 'remove'"
            return
        case.print_id()
        self._get_case_path(case)

        self.select_test_plan(test_plan)
        self.browser.find_element(
            By.LINK_TEXT, "Add / Remove Test Cases").click()
        time.sleep(2)

        self.switch_to_treeframe()
        tree = Tree(self.browser, self.logger)
        tree.expand_case(case)

        self.switch_to_workframe()
        table = AddRemoveTable(self.browser, self.logger)
        try:
            table.move_case_for_platform(action=action, case=case,
                                         platform=platform)

        except FolderNotFoundError as err:
            print ("Error found when trying to {a} case: {c}"
                   .format(a=action, c=case.case_id))
            print err

    def update_case_version(self, case, test_plan):
        case.print_id()
        self._get_case_path(case)

        self.select_test_plan(test_plan)
        self.browser.find_element(
            By.LINK_TEXT, "Update Linked Test Case Versions").click()
        time.sleep(2)

        self.switch_to_treeframe()
        tree = Tree(self.browser, self.logger)
        tree.expand_case(case)

        self.switch_to_workframe()
        table = VersionTable(self.browser, self.logger)
        table.update_case_version(case)

    def update_case_folder(self, case_folder_path, test_plan):
        self.select_test_plan(test_plan)
        self.browser.find_element(
            By.LINK_TEXT, "Update Linked Test Case Versions").click()
        time.sleep(2)

        self.switch_to_treeframe()
        tree = Tree(self.browser, self.logger)
        tree.expand_folder_path(case_folder_path)

        self.switch_to_workframe()
        table = VersionTable(self.browser, self.logger)
        table.update_folder_version(case_folder_path)

    def assign_case(self, case, tester, test_plan, platform):
        case.print_id()
        self._get_case_path(case)

        self.select_test_plan(test_plan)
        self.browser.find_element(
            By.LINK_TEXT, "Assign Test Case Execution").click()
        time.sleep(2)

        self.switch_to_treeframe()
        tree = Tree(self.browser, self.logger)
        tree.expand_case(case)

        self.switch_to_workframe()
        table = AssignTable(self.browser, self.logger)
        table.assign_case_to_tester(case, tester, platform)


