Webdriver Helper to Testlink Actions
====================================

quick start:

    Download and put all files and unzipped selenium in same folder

    Usage:

    To set urgency of test cases to Low:
    python set_test_cases.py --action=1 --priority=Low --testplan=6.0.1 -f <your_case_list>

    To priority of test cases to High:
    python set_test_cases.py --action=2 --priority=High -f <your_case_list>

    To add test cases to a testplan and platform
	python set_test_cases.py --action=3 --platform="Integrated Platform" --testplan=6.0.1 -f <your_case_list>

	To remove test cases from a testplan and platform
	python set_test_cases.py --action=4 --platform="Integrated Platform" --testplan=6.0.1 -f <your_case_list>

	To assign test cases to wythe
	python set_test_cases.py --action=4 --platform="Integrated Platform" --testplan=6.0.1 --assignee=clin -f <your_case_list>


 - Set priority of specified cases
 - Update version of specified case in testplan
 - Add/Remove specified case from testplan
 - Assign specified case of specified platform to tester in testplan
 - You can assign your specified cases in your file with comment
