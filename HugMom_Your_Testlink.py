import getopt
import sys
import errno
from TestlinkWeb import TestlinkCase
from TestlinkWeb import TestlinkWeb
import re
import string
import getpass


def main():
    # --high          : Change priority of testcases to High (default setting)
    #                   ex: python ./Modify_Testcase_Priority.py --high
    # -m, --medium    : Change priority of testcases to Medium
    #                   ex: python ./Modify_Testcase_Priority.py -m
    #                       python ./Modify_Testcase_Priority.py --medium
    """
    -f, --file      : Execute cases list in the specified file
                      ex: python ./Modify_Testcase_Priority.py -f ./<your_file>.txt
                          python ./Modify_Testcase_Priority.py --file=<your_file>.txt
    -h, --help      : Argument usage
                      ex: python ./Modify_Testcase_Priority.py -h
                          python ./Modify_Testcase_Priority.py --help
    """
    #testcases_id = ["0800", "092", "000"]
    testcases_id = ["3317"]
    #testcases_id = map(str, range(625, 631))
    # testcases_id.append("863")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:h",
                                   ["help", "file="])
    except getopt.error as err:
        print "ERROR: " + str(err)
        print "for argument usage, use -h or --help"
        print main.__doc__
        sys.exit(errno.EINVAL)

    for key, value in opts:
        if key in ("-h", "--help"):
            print main.__doc__
            sys.exit()
        # elif key in ("--high"):
        #     priority_key = "High"
        # elif key in ("-m", "--medium"):
        #     priority_key = "Medium"
        elif key in ("-f", "--file"):
            CASES_FILE = str(value)
            try:
                with open(CASES_FILE, "r") as cases_file:
                    testcases_id = [re.search("\d+", case.strip()).group()
                                    for case in cases_file.readlines()
                                    if case.startswith("splunk") or
                                    case.startswith(tuple(string.digits))]
            except IOError as err:
                print err
                sys.exit(errno.EINVAL)
        else:
            assert False, "unhandled option"

    LOGIN_NAME = raw_input("Please enter your testlink login name: ")
    LOGIN_PWD = getpass.getpass("Please enter your testlink login password: ")

    # If you dont wanna type login name/pwd, just comment out lines above
    # and assigned LOGIN_NAME/LOGIN_PWD directly, NOT RECOMMENDED for security
    testlink_web = TestlinkWeb()
    if testlink_web.login(LOGIN_NAME, LOGIN_PWD):

        # Set Priority ("High" or "Medium") Example:
        priority_key = "High"
        for case_id in testcases_id:
            case = TestlinkCase(case_id)
            testlink_web.setPriority(case, priority_key)

        # Update Case in Test Plan Example:
        # for case_id in testcases_id:
        #     case = TestlinkCase(case_id)
        #     testlink_web.updateCaseInPlan(case, "6.0.2")

        # Add/Remove Case from Test Plan Example:
        # for case_id in testcases_id:
        #     case = TestlinkCase(case_id)
        #     # for remove: testlink_web.moveCaseForPlan(case, "remove", "6.0.2")
        #     testlink_web.moveCaseForPlan(case, "add", "6.0.2")

    else:
        print ("your login name/password seems invalid, "
               "please check and input again")
        sys.exit(errno.EINVAL)

if __name__ == "__main__":
    main()
