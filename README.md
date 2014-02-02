Webdriver Helper to Testlink Actions
====================================

quick start:

    Download and put all files and unzipped selenium in same folder

    Usage:
    Helper text:  python Set_Cases_Actions.py -h

    Recommend:  python Set_Cases_Actions.py <your_case_list.txt> -i

    (valid format for optional arguments: --<args>=<value>/--<args> <value>)
    (multiple actions (in space format) are acceptable: --action 2 3 / -a 2 3)

    To set urgency of testcases to Low in a testplan:
    python Set_Cases_Actions.py <your_case_list.txt> --action=1 --priority=Low --testplan=6.0.1

    To set priority of testcases to High:
    python Set_Cases_Actions.py <your_case_list.txt> --action=2 --priority=High

    To update version of testcases in a testplan:
    python Set_Cases_Actions.py <your_case_list.txt> --action=3 --testplan=6.0.1

    To add testcases to a testplan on a platform:
    python Set_Cases_Actions.py <your_case_list.txt> --action=4 --testplan=6.0.1
    --platform="Integrated Platform"/''/"Firefox + Linux"

    To remove testcases from a testplan on a platform:
    python Set_Cases_Actions.py <your_case_list.txt> --action=5 --testplan=6.0.1
    --platform="Integrated Platform"/''/"Firefox + Linux"

    To assign testcases to a tester:
    python Set_Cases_Actions.py <your_case_list.txt> --action=6 --testplan=6.0.1
    --platform="Integrated Platform"/''/"Firefox + Linux" --assignee=clin


 - Set urgency of cases (plan-based)
 - Set priority of cases (case-based)
 - Update version of cases in testplan
 - Add/Remove cases for a testplan on a platform
 - Assign cases on a platform to tester in a testplan
 - You need to specify your cases id in a file, may with comment
