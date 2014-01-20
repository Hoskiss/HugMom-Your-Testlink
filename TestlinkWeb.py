from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import os
import logging
import re
import string


class TestlinkCase(object):

    def __init__(self, case_id):
        self.case_id = case_id


class TestlinkWeb(object):
    """
    Version: 0.3 / 2014.01.20
        - set case priority
        - add/remove case for testplan
        - update case version in testplan
    """

    def __init__(self, browser=None):
        self.URL = "http://testlink.splunk.com/index.php"
        self.PRIORITY_MAP = {"High": "3",
                             "Medium": "2"}
        self.browser = browser or webdriver.Firefox()

        # logging
        file_name = os.path.basename(__file__).split(".")[0]
        logger = logging.getLogger(file_name)
        logger.setLevel(logging.DEBUG)

        # create a file handler
        handler = logging.FileHandler(file_name + '.log', mode='w')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(handler)
        self.logger = logger

    def login(self, login_user, login_pwd):
        self.browser.get(self.URL)
        self.browser.find_element(By.ID, "login").send_keys(login_user)
        self.browser.find_element(By.NAME, "tl_password").send_keys(
            login_pwd + Keys.RETURN)
        time.sleep(2)
        try:
            # login failed
            self.browser.find_element(By.ID, "login")
            return False
        except:
            return True

    def openCase(self, case):
        self.browser.get(self.URL)
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("titlebar")
        input_id = self.browser.find_element(By.NAME, "targetTestCase")
        input_id.clear()
        input_id.send_keys("splunk-" + case.case_id + Keys.RETURN)
        time.sleep(2)
        print "Open {c_id}:".format(c_id=case.case_id)
        self.logger.info("Open {c_id}:".format(c_id=case.case_id))

    def setPriority(self, case, priority="High"):
        self.openCase(case)

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
                self.browser.find_element(
                    By.NAME, "do_create_new_version").click()
                time.sleep(2)
                self.browser.find_element(By.NAME, "edit_tc").click()
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

    def selectTestPlan(self, which_plan="6.0.2"):
        self.browser.get(self.URL)
        time.sleep(2)

        # select test project
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("titlebar")
        Select(self.browser.find_element(By.NAME, "testproject")
               ).select_by_value("1")
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        Select(self.browser.find_element(By.NAME,
            "testplan")).select_by_visible_text(
            "{which_plan} Test Plan".format(which_plan=which_plan))
        time.sleep(2)

    def getCasePath(self, case):
        self.openCase(case)
        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")

        get_path = self.browser.find_element(
            By.CSS_SELECTOR, "div.workBack h2").text.split("/")
        # path rule: first part is global "splunk"
        #           second part is test suite, ex: "UI"
        #           last one is case name
        case.test_suite = get_path[1].strip()
        case.full_name = get_path[-1].strip()
        case.name = re.search("splunk-\d+:(?P<name>.+)",
                              case.full_name).group('name').strip()
        case.sub_path = [part.strip() for part in get_path]
        case.sub_path = case.sub_path[2:-1]

        self.logger.debug("*" * 15)
        self.logger.debug("case.case_id: " + case.case_id)
        self.logger.debug("case.test_suite: " + case.test_suite)
        self.logger.debug("case.full_name: " + case.full_name)
        self.logger.debug("case.name: " + case.name)
        self.logger.debug("case.sub_path: " + str(case.sub_path))
        self.logger.debug("*" * 15)

    def moveCaseForPlan(self, case, add_or_remove, which_plan="6.0.2",
                        platform="Integrated platform"):
        if "add" != add_or_remove and "remove" != add_or_remove:
            print "check your second parameter, should be 'add' or 'remove'"
            return

        self.getCasePath(case)
        self.selectTestPlan(which_plan)

        self.browser.find_element(
            By.LINK_TEXT, "Add / Remove Test Cases").click()
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        self.browser.switch_to_frame("treeframe")

        # try filter!
        Select(self.browser.find_element(By.NAME,
            "filter_toplevel_testsuite")).select_by_visible_text(
            "{test_suite}".format(test_suite=case.test_suite))
        # Select(self.browser.find_element(By.NAME,
        #    "filter_execution_type")).select_by_visible_text("Automated")
        self.browser.find_element(
            By.CSS_SELECTOR, "input#doUpdateTree").click()
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, "input#expand_tree").click()
        time.sleep(2)

        including_folders = self.browser.find_elements(
            By.PARTIAL_LINK_TEXT, case.sub_path[-1])

        for each_folder in including_folders:
            self.browser.switch_to_default_content()
            self.browser.switch_to_frame("mainframe")
            self.browser.switch_to_frame("treeframe")
            each_folder.click()
            time.sleep(2)

            self.browser.switch_to_default_content()
            self.browser.switch_to_frame("mainframe")
            self.browser.switch_to_frame("workframe")

            try:
                Select(self.browser.find_element(By.ID,
                        "select_platform")).select_by_visible_text(platform)
            #no cases under this folder
            except:
                continue

            elem = self.waitForElement(By.PARTIAL_LINK_TEXT, case.name)
            if elem is None:
                continue
            else:
                tooltip_count = elem.get_attribute("href")
                tooltip_count = re.search("\d+", tooltip_count).group()
                self.logger.debug("tooltip_count: " + tooltip_count)
                break

        assert(tooltip_count is not None)

        if "add" == add_or_remove:
            checkbox_id = "achecked_tc{count}".format(count=tooltip_count)
        else:
            checkbox_id = "remove_checked_tc{count}[17]".format(count=tooltip_count)

        try:
            self.browser.find_element(By.ID, checkbox_id).click()
        except:
            print "check if {case} has been {a_o_r} already in {plan}!".format(
                case=case.full_name, a_o_r=add_or_remove, plan=which_plan)
            self.logger.info( "check if {case} has been {a_o_r} already in {plan}!".format(
                case=case.full_name, a_o_r=add_or_remove, plan=which_plan) )
            return

        self.browser.find_element(By.NAME, "doAddRemove").click()
        time.sleep(2)
        print "{a_o_r} < {full_path} / {full_name} > from {plan} {platform}!".format(
            a_o_r=add_or_remove,
            full_path=case.test_suite + "/" + "/".join(case.sub_path),
            full_name=case.full_name,
            plan=which_plan,
            platform=platform)
        self.logger.info( "{a_o_r} < {full_path} / {full_name} > from {plan} {platform}!".format(
            a_o_r=add_or_remove,
            full_path=case.test_suite+"/"+"/".join(case.sub_path),
            full_name=case.full_name,
            plan=which_plan,
            platform=platform) )

    def waitForElement(self, by_what, specified_value, timeout=10):
        while timeout != 0:
            try:
                found_element = self.browser.find_element(by_what, specified_value)
                return found_element
            except Exception as err:
                time.sleep(1)
                timeout -= 1
        return None

    def updateCaseInPlan(self, case, which_plan="6.0.2"):
        self.getCasePath(case)
        self.selectTestPlan(which_plan)

        self.browser.find_element(
            By.LINK_TEXT, "Update Linked Test Case Versions").click()
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        self.browser.switch_to_frame("treeframe")

        Select(self.browser.find_element(By.NAME,
            "filter_toplevel_testsuite")).select_by_visible_text(
            "{test_suite}".format(test_suite=case.test_suite))

        self.browser.find_element(
            By.CSS_SELECTOR, "input#doUpdateTree").click()
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, "input#expand_tree").click()
        time.sleep(2)

        including_folders = self.browser.find_elements(
            By.PARTIAL_LINK_TEXT, case.sub_path[-1])

        for each_folder in including_folders:
            self.browser.switch_to_default_content()
            self.browser.switch_to_frame("mainframe")
            self.browser.switch_to_frame("treeframe")
            each_folder.click()
            time.sleep(2)

            self.browser.switch_to_default_content()
            self.browser.switch_to_frame("mainframe")
            self.browser.switch_to_frame("workframe")

            elem = self.waitForElement(By.PARTIAL_LINK_TEXT, case.name)
            if elem is None:
                continue
            else:
                tooltip_count = elem.get_attribute("href")
                tooltip_count = re.search("\d+", tooltip_count).group()
                self.logger.debug("tooltip_count: " + tooltip_count)
                break

        assert(tooltip_count is not None)
        update_checkbox_id = "achecked_tc{count}".format(
            count=tooltip_count)
        self.browser.find_element(By.ID, update_checkbox_id).click()
        self.browser.find_element(By.ID, "update_btn").click()
        time.sleep(2)
        print "update < {full_path} / {full_name} > in {plan}!".format(
            full_path=case.test_suite + "/" + "/".join(case.sub_path),
            full_name=case.full_name,
            plan=which_plan)
        self.logger.info( "update < {full_path} / {full_name} > in {plan}!".format(
            full_path=case.test_suite+"/"+"/".join(case.sub_path),
            full_name=case.full_name,
            plan=which_plan) )

    # Don't use this function for now, cause of multiple same name folder!
    def updateCaseFolderInPlan(self, case_folder, test_suite="", which_plan="6.0.2"):
        self.selectTestPlan(which_plan)

        self.browser.find_element(
            By.LINK_TEXT, "Update Linked Test Case Versions").click()
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        self.browser.switch_to_frame("treeframe")

        # case_folder_path = map(string.strip, case_folder.split("/"))
        # print "case_folder_path: " + str(case_folder_path)
        # self.logger.info("case_folder_path: " + str(case_folder_path))

        Select(self.browser.find_element(By.NAME,
            "filter_toplevel_testsuite")).select_by_visible_text(
            "{test_suite}".format(test_suite=test_suite))

        self.browser.find_element(
            By.CSS_SELECTOR, "input#doUpdateTree").click()
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, "input#expand_tree").click()
        time.sleep(2)

        case_folder = case_folder.strip()

        timeout = 10
        while timeout != 0:
            try:
                self.browser.find_element(
                    By.PARTIAL_LINK_TEXT, case_folder).click()
                break
            except Exception as err:
                time.sleep(1)
                timeout -= 1
        time.sleep(2)

        self.browser.switch_to_default_content()
        self.browser.switch_to_frame("mainframe")
        self.browser.switch_to_frame("workframe")

        timeout = 10
        while timeout != 0:
            try:
                title_folder = self.browser.find_element(By.CSS_SELECTOR,
                    "div.workBack h3").text
                self.logger.info(title_folder)
                assert(case_folder in title_folder)
                break
            except Exception as err:
                time.sleep(1)
                timeout -= 1

        self.browser.find_element(By.CSS_SELECTOR,
            "div.workBack h3.testlink img").click()
        self.browser.find_element(By.ID, "update_btn").click()
        time.sleep(2)
        print "update < {folder_path} > in {plan}!".format(
            folder_path=case_folder, plan=which_plan)
        self.logger.info( "update < {folder_path} > in {plan}!".format(
            folder_path=case_folder, plan=which_plan) )
