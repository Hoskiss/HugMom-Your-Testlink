from TestlinkWeb import TestlinkCase
from TestlinkWeb import TestlinkWeb
import getpass
import optparse


def main():
    """
    Main process
    """
    LOGIN_NAME = raw_input("Please enter your testlink login name: ")
    LOGIN_PWD = getpass.getpass("Please enter your testlink login password: ")

    testlink_web = TestlinkWeb()
    # if testlink_web.login(LOGIN_NAME, LOGIN_PWD):


if __name__ == '__main__':
    # LOGIN_NAME = raw_input("Please enter your testlink login name: ")
    # LOGIN_PWD = getpass.getpass("Please enter your testlink login password: ")
    LOGIN_NAME = "clin"
    LOGIN_PWD = "2jiidgli"

    testlink_web = TestlinkWeb()
    testlink_web.login(LOGIN_NAME, LOGIN_PWD)

    case = TestlinkCase("1002")
    testlink_web.getCasePath(case)

    testlink_web.open_urgency_page("5.0.5")
