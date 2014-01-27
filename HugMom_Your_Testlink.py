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
    #                   ex: python ./HugMom_Your_Testlink.py --high
    # -m, --medium    : Change priority of testcases to Medium
    #                   ex: python ./HugMom_Your_Testlink.py -m
    #                       python ./HugMom_Your_Testlink.py --medium
    """
    -f, --file      : Execute cases list in the specified file
                      ex: python ./HugMom_Your_Testlink.py -f ./<your_file>.txt
                          python ./HugMom_Your_Testlink.py --file=<your_file>.txt
    -h, --help      : Argument usage
                      ex: python ./HugMom_Your_Testlink.py -h
                          python ./HugMom_Your_Testlink.py --help
    """
    #testcases_id = ["0800", "092", "000"]
    #testcases_id = map(str, range(625, 631))
    # testcases_id.append("863")
    testcases_id = ["1809"]
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


        for case_id in testcases_id:
            # case = TestlinkCase(case_id)
            # testlink_web.update_case_version(case, which_plan="6.0.1")

            # folder_path = ["CLI commands", "deployment client/server"]
            # testlink_web.update_case_folder(folder_path, "6.0.1")

            case = TestlinkCase(case_id)
            testlink_web.move_case(case, "remove", "6.0.1", "Integrated platform")

            ## Set Priority ("High" or "Medium") Example:
            # priority_key = "High"
            # testlink_web.setPriority(case, priority_key)

            ## Update Case in Test Plan Example:
            # testlink_web.updateCaseInPlan(case, "6.0.2")

            ## Add/Remove Case from Test Plan Example:
            ## For remove: testlink_web.moveCaseForPlan(case, "remove", "6.0.2")
            # testlink_web.moveCaseForPlan(case, "remove", "6.0.2")

            ## Assign Case to Tester in Test Plan Example:
            # testlink_web.assignCaseInPlan(case, "to_whom", "6.0.2", "Integrated platform")

    else:
        sys.exit(errno.EINVAL)

if __name__ == "__main__":
    main()
