from TestlinkWeb import TestlinkCase
from TestlinkWeb import TestlinkWeb
import errno
from optparse import OptionParser
import string
import re
import getpass
import sys
from collections import OrderedDict

d = {"1": "urgency", "2": "priority", "3": "add", "4": "remove", "5": "assign"}
ACTION_MAP = OrderedDict(sorted(d.items(), key=lambda t:t[0]))

ACTION_HELP_STRING =(
'''
 1: set urgency for testcases
 2: set priority for testcases
 3: add testcases to a testplan
 4: remove testcases from a testplan
 5: assign testcases to somebody
 ''')

def get_login_credential():
    """
    Get login credential from stdin
    """
    LOGIN_NAME = raw_input("Please enter your testlink login name: ")
    LOGIN_PWD = getpass.getpass("Please enter your testlink login password: ")

    return (LOGIN_NAME, LOGIN_PWD)

def get_testcases(file_name):
    """
    Get testcase ids in given file
    """
    # get list of testcases
    if file_name is None:
        print "You must specify a file which listing testcases"
        sys.exit(errno.EINVAL)

    try:
        with open(file_name, "r") as cases_file:
            testcases_id = [re.search("\d+", case.strip()).group()
                            for case in cases_file.readlines()
                            if case.startswith("splunk") or
                            case.startswith(tuple(string.digits))]
    except IOError as err:
        print err
        sys.exit(errno.EINVAL)

    return [TestlinkCase(tid) for tid in testcases_id]

def parse_options():
    """
    parse options
    """
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                      help="the input file which lists testcase ids")
    parser.add_option("-p", "--priority", dest="priority",
                      help="the priority for setting urgency or priority")
    parser.add_option("-t", "--testplan", dest="testplan",
                      help="the testplan for setting urgency or"
                           " add/remove/assign testcases")
    parser.add_option("-u", "--assignee", dest="assignee",
                      help="assignee when assigning testcases")
    parser.add_option("-a", "--action", dest="action",
                      help=ACTION_HELP_STRING)
    parser.add_option("-l", "--platform", dest="platform",
                      help="platform for assigning test case",
                      default=None)
    (options, args) = parser.parse_args()
    return options

def get_priority(priority):
    """
    translate user's priority to the format tha TestlinkWeb can recognize
    """
    if priority.capitalize() in ["High", "Medium", "Low"]:
        return priority.capitalize()
    elif priority is None:
        print "Priority is no given"
        sys.exit(errno.EINVAL)
    else:
        print "{p} is not supported for priority".format(p=priority)
        sys.exit(errno.EINVAL)

def main():
    """
    main process
    """
    options = parse_options()

    # check action argument is correct
    if not options.action in ACTION_MAP.keys():
        print ("{o} is not implemented, please select one of {k}"
               " as action parameter".format(o=options.action,
                                            k=str(ACTION_MAP.keys())))
        sys.exit(errno.EINVAL)

    test_cases = get_testcases(options.file)
    (user, pwd) = get_login_credential()
    testlink = TestlinkWeb()

    if testlink.login(user, pwd):
        if "urgency" == ACTION_MAP[options.action]:
            if options.testplan is None:
                print "testplan is required when setting urgency"
                sys.exit(errno.EINVAL)

            if options.priority is None:
                print "priority is required when setting urgency"
                sys.exit(errno.EINVAL)

            priority = get_priority(options.priority)
            print "Setting urgency for your test cases"
            for test_case in test_cases:
                testlink.set_case_urgency(test_plan=options.testplan,
                                          case=test_case,
                                          urgency=priority)

        elif "priority" == ACTION_MAP[options.action]:
            if options.priority is None:
                print "priority is required when setting priority"
                sys.exit(errno.EINVAL)

            priority = get_priority(options.priority)
            print "Setting priority for your test cases"
            for test_case in test_cases:
                testlink.set_case_priority(test_case, priority)

        elif "add" == ACTION_MAP[options.action]:
            print "Adding test cases to your testplan: " + options.testplan
            for test_case in test_cases:
                testlink.move_case(test_case, "add", options.testplan,
                                        options.platform)

        elif "remove" == ACTION_MAP[options.action]:
            print "Removing test cases from your testplan: " + options.testplan
            for test_case in test_cases:
                testlink.move_case(test_case, "remove", options.testplan,
                                        options.platform)

        elif "assign" == ACTION_MAP[options.action]:
            if options.assignee is None:
                print "you must specify a user as assignee"
                sys.exit(errno.EINVAL)

            if options.testplan is None:
                print "you must specify which testplan to assign testcases"
                sys.exit(errno.EINVAL)

            for test_case in test_cases:
                testlink.assign_case(test_case, options.assignee,
                                     options.testplan, options.platform)

        print "DONE"
    else:
        print ("your login name/password seems invalid, "
               "please check and input again")
        sys.exit(errno.EINVAL)

if __name__ == '__main__':
    main()
