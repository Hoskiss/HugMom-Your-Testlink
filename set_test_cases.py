from TestlinkWeb import TestlinkCase
from TestlinkWeb import TestlinkWeb
import errno
from optparse import OptionParser


def get_testcases(file_name):
    """
    Get testcase ids in given file
    """
    # get list of testcases
    try:
        with open(CASES_FILE, "r") as cases_file:
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
                      help="should be in [priority, urgency, add, remove]")
    (options, args) = parser.parse_args()
    return options

def main():
    """
    main process
    """
    options = parse_options()

    # get testcases
    test_cases = get_testcases(options.file)
    testlink = TestlinkWeb()

    if testlink.login()
        if "urgency" == options.action:
            if options.testplan is None:
                print "testplan is required when setting urgency"
                sys.exit(errno.EINVAL)

            if options.priority is None:
                print "priority is required when setting urgency"
                sys.exit(errno.EINVAL)

            for test_case in test_cases:
                testlink.setCaseUrgency(test_plan=options.testplan,
                                        case=test_case,
                                        urgency=options.priority)

        elif "priority" == options.action:
            if options.priority is None:
                print "priority is required when setting priority"
                sys.exit(errno.EINVAL)

            for test_case in test_cases:
                testlink.setPriority(test_case, options.priority)

        elif "add" == options.action:
            if options.testplan is None:
                print "you must specify which testplan to add testcases to"
                sys.exit(errno.EINVAL)

            for test_case in test_cases:
                testlink.moveCaseForPlan(test_case, "add", options.testplan)

        elif "remove" == options.action:
            if options.testplan is None:
                print "you must specify which testplan to remove testcases from"
                sys.exit(errno.EINVAL)

            for test_case in test_cases:
                testlink.moveCaseForPlan(test_case, "remove", options.testplan)
        else:
            print ("{o} is not implemented,"
                   " please select one of [priority, urgency, add, remove]"
                   "as action parameter".format(o=options.action))
            sys.exit(errno.EINVAL)

    else:
        print ("your login name/password seems invalid, "
               "please check and input again")
        sys.exit(errno.EINVAL)

if __name__ == '__main__':
    main()