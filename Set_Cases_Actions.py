from TestlinkWeb import TestlinkCase
from TestlinkWeb import TestlinkWeb
import errno
import string
import re
import getpass
import sys
import argparse
from argparse import RawTextHelpFormatter

ACTION_MAP = {"1": "urgency", "2": "priority",
              "3": "update", "4": "add",
              "5": "remove", "6": "assign"}
#ACTION_MAP = OrderedDict(sorted(act.items(), key=lambda t: t[0]))

ACTION_HELP_STRING = '''
1: set urgency for testcases
   (need priority, testplan)
2: set priority for testcases
   (need priority)
3: update version of cases in a testplan
   (need testplan)
4: add testcases in a testplan
   (need testplan, platform)
5: remove testcases in a testplan
   (need testplan, platform)
6: assign testcases to somebody
   (need testplan, platform, assignee)
'''

def parse_arguments():
    """
    parse options for actions
    """
    parser = argparse.ArgumentParser(
        description="Run webdriver helper to actions on testlink cases",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument("file", type=argparse.FileType('r'),
                        help="the input file which lists testcase ids \n" +
                        "example values: ExampleCaseList.txt")

    parser.add_argument("-a", "--action", help="Select action on cases, ex: -a 2 3" +
                        ACTION_HELP_STRING, choices=map(str, range(1, 7)),
                        nargs='+', metavar='', dest="action")
    priority_choice = ["l", "L", "m", "M", "h", "H",
                       "low", "Low", "medium", "Medium", "high", "High"]
    parser.add_argument("-p", "--priority", choices=priority_choice, metavar='',
                        help="set priority to cases, allowed values are \n" +
                        ", ".join(priority_choice), dest="priority")
    parser.add_argument("-n", "--testplan", help="set cases in which testplan \n" +
                        "example values: 6.0.2", metavar='', dest="testplan")
    parser.add_argument("-m", "--platform", help="set cases in which platform \n" +
                        "example values: Integrated platform, '', Firefox + Linux",
                        metavar='', dest="platform")
    parser.add_argument("-e", "--assignee", help="assign cases to whom \n" +
                        "example values: clin", metavar='', dest="assignee")

    parser.add_argument("-i", "--interactive", help="interactive way to set "+
                        "actions on testcases", action="store_true")

    return parser.parse_args()

def get_testcases(in_file):
    """
    Get testcase ids in given file
    """
    try:
        #with open(file_name, "r") as cases_file:
        testcases_id = [re.search("\d+", case.strip()).group()
                        for case in in_file.readlines()
                        if case.startswith("splunk") or
                        case.startswith(tuple(string.digits))]
    except IOError as err:
        print err
        sys.exit(errno.EINVAL)

    return [TestlinkCase(tid) for tid in testcases_id]

def check_interactive_args(args):
    if args.interactive:
        args.action = []
        action_idx = raw_input("Please select actions on case: "
                               "(multiple actions accepted, ex: 23) \n" +
                               ACTION_HELP_STRING)
        for idx in action_idx:
            if idx not in map(str, range(1, 7)):
                print ("Invalid selection of actions,\n" +
                       "your selection of actions must between 1 to 6!")
                sys.exit(errno.EINVAL)

            args.action.append(idx)
            if "urgency" == ACTION_MAP[idx]:
                if args.testplan is None:
                    args.testplan = raw_input("Please enter action in " +
                                              "which testplan, ex: 6.0.2\n")
                if args.priority is None:
                    args.priority = raw_input("Please enter which priority " +
                                              "level, ex: high/medium/low\n")

            elif "priority" == ACTION_MAP[idx]:
                if args.priority is None:
                    args.priority = raw_input("Please enter which priority " +
                                              "level, ex: high/medium/low\n")

            elif "update" == ACTION_MAP[idx]:
                if args.testplan is None:
                    args.testplan = raw_input("Please enter action in " +
                                              "which testplan, ex: 6.0.2\n")

            elif "add" == ACTION_MAP[idx]:
                if args.testplan is None:
                    args.testplan = raw_input("Please enter action in " +
                                              "which testplan, ex: 6.0.2\n")
                if args.platform is None:
                    args.platform = raw_input("Please enter action in which platform, " +
                                              "ex: Integrated platform/''/Firefox + Linux\n")

            elif "remove" == ACTION_MAP[idx]:
                if args.testplan is None:
                    args.testplan = raw_input("Please enter action in " +
                                              "which testplan, ex: 6.0.2\n")
                if args.platform is None:
                    args.platform = raw_input("Please enter action in which platform, " +
                                              "ex: Integrated platform/''/Firefox + Linux\n")

            elif "assign" == ACTION_MAP[idx]:
                if args.testplan is None:
                    args.testplan = raw_input("Please enter action in " +
                                              "which testplan, ex: 6.0.2\n")
                if args.platform is None:
                    args.platform = raw_input("Please enter action in which platform, " +
                                              "ex: Integrated platform/''/Firefox + Linux\n")
                if args.assignee is None:
                    args.assignee = raw_input("Please enter assignee who take cases, ex: hlin\n")

def check_valid_args(args):
    for act_idx in args.action:
        if "urgency" == ACTION_MAP[act_idx]:
            if args.testplan is not None and args.priority is not None:
                continue
            if args.testplan is None:
                print ("testplan is required when setting urgency,\n"
                       "add argument -n, --testplan <ex: 6.0.2>")
            if args.priority is None:
                print ("priority level is required when setting urgency,\n"
                       "add argument -p, --priority <ex: high>")
            sys.exit(errno.EINVAL)

        elif "priority" == ACTION_MAP[act_idx]:
            if args.priority is None:
                print ("priority level is required when setting priority,\n"
                       "add argument -p, --priority <ex: high>")
                sys.exit(errno.EINVAL)

        elif "update" == ACTION_MAP[act_idx]:
            if args.testplan is None:
                print ("testplan is required when updating case version,\n"
                       "add argument -n, --testplan <ex: 6.0.2>")
                sys.exit(errno.EINVAL)

        elif "add" == ACTION_MAP[act_idx]:
            if args.testplan is not None and args.platform is not None:
                continue
            if args.testplan is None:
                print ("testplan is required when adding case,\n"
                       "add argument -n, --testplan <ex: 6.0.2>")
            if args.platform is None:
                print ("platform is required when adding case,\n"
                       "add argument -m, --platform <ex: Integrated platform>")
            sys.exit(errno.EINVAL)

        elif "remove" == ACTION_MAP[act_idx]:
            if args.testplan is not None and args.platform is not None:
                continue
            if args.testplan is None:
                print ("testplan is required when removing case,\n"
                       "add argument -n, --testplan <ex: 6.0.2>")
            if args.platform is None:
                print ("platform is required when removing case,\n"
                       "add argument -m, --platform <ex: Integrated platform>")
            sys.exit(errno.EINVAL)

        elif "assign" == ACTION_MAP[act_idx]:
            if (args.testplan is not None and
                args.platform is not None and
                args.assignee is not None):
                continue
            if args.testplan is None:
                print ("testplan is required when assigning case,\n"
                       "add argument -n, --testplan <ex: 6.0.2>")
            if args.platform is None:
                print ("platform is required when assigning case,\n"
                       "add argument -m, --platform <ex: Integrated platform>")
            if args.assignee is None:
                print ("assignee is required when assigning case,\n"
                       "add argument -e, --assignee <ex: clin>")
            sys.exit(errno.EINVAL)

def get_login_credential():
    """
    Get login credential from stdin
    """
    LOGIN_NAME = raw_input("Please enter your testlink login name: ")
    LOGIN_PWD = getpass.getpass("Please enter your testlink login password: ")

    return {"name": LOGIN_NAME, "pwd": LOGIN_PWD}

def classify_priority(priority):
    if priority in ["l", "L", "low", "Low"]:
        return "Low"
    elif priority in ["m", "M", "medium", "Medium"]:
        return "Medium"
    elif priority in ["h", "H", "high", "High"]:
        return "High"
    else:
        raise ("Invalid Priority")

def main():
    """
    main process
    """
    args = parse_arguments()
    check_interactive_args(args)
    check_valid_args(args)
    testcases = get_testcases(args.file)
    #print args

    credential = get_login_credential()
    testlink = TestlinkWeb()
    if not testlink.login(credential["name"], credential["pwd"]):
        print ("your login name/password seems invalid, "
               "please check and input again")
        sys.exit(errno.EINVAL)

    for case in testcases:
        for act_idx in args.action:
            if "urgency" == ACTION_MAP[str(act_idx)]:
                testlink.set_case_urgency(case,
                                          args.testplan,
                                          classify_priority(args.priority))

            elif "priority" == ACTION_MAP[str(act_idx)]:
                testlink.set_case_priority(case,
                                           classify_priority(args.priority))

            elif "update" == ACTION_MAP[str(act_idx)]:
                testlink.update_case_version(case, args.testplan)

            elif "add" == ACTION_MAP[str(act_idx)]:
                testlink.move_case(case, "add", args.testplan,
                                   args.platform)

            elif "remove" == ACTION_MAP[str(act_idx)]:
                testlink.move_case(case, "remove", args.testplan,
                                   args.platform)

            elif "assign" == ACTION_MAP[str(act_idx)]:
                testlink.assign_case(case, args.assignee,
                                     args.testplan, args.platform)

    print "DONE"

if __name__ == '__main__':
    main()
