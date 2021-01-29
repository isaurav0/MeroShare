#! /usr/local/bin/python3
import sys
from meroshare import MeroShare

LOGIN = 'login'
BANKS = 'banks'
ISSUES = 'issues'
COMPANY = 'company'
REPORTS = 'reports'
ALL_REPORTS = 'all_reports'
RESULT = 'result'
LOGOUT = 'logout'

help_message=f'''

    A command line tool to get meroshare details

    Usage: meroshare [option] [optional_options]

    Viewing banks
        $ meroshare {BANKS}

    Logging in
        $ meroshare {LOGIN}

        requires username, password and bank_id or bank_name
        bank details can be found from
            $ meroshare {BANKS}
        command.

    Viewing current issues
        $ meroshare {ISSUES}

    Viewing company details
        $ meroshare {COMPANY} [company_id]
        [company_id] can be found from issues and reports

    Viewing recent submitted applications
        $ meroshare {REPORTS}

    Viewing all submitted applications
        $ meroshare {ALL_REPORTS}

    Viewing result of applied share
        $ meroshare {RESULT} [form_id]
        [form_id] can be found from [reports] switch

    Logging out
        $ meroshare {LOGOUT}

'''

def main():

    if len(sys.argv) < 2:
        print(help_message)
        exit()

    option = sys.argv[1]

    if option == BANKS:
        share = MeroShare(defaultLogin=False)
        share.getBanks().printBanks()
        return

    share = MeroShare(defaultLogin=True)

    if option == LOGIN:
        pass

    elif option == ISSUES:
        share.getCurrentIssues().printIssues()

    elif option == REPORTS:
        share.getApplicationReport().printApplicationReport()

    elif option == ALL_REPORTS:
        share.getOldApplicationReport().printApplicationReport()

    elif option == COMPANY:
        if len(sys.argv) < 3:
            print("Error: Company Id not supplied! ")
            print(help_message)
            exit()

        cid = sys.argv[2]
        share.getCompanyDetails(cid).printCompanyDetails()

    elif option == LOGOUT:
        share.eraseCredentials()
        print('Logged Out.')

    elif option == RESULT:
        if len(sys.argv) < 3:
            print("Error: Form Id not supplied! ")
            print(help_message)
            exit()

        fid = sys.argv[2]
        share.getFormDetails(fid).printFormDetails()

    else:
        print(help_message)
        exit()


if __name__ == '__main__':
    main()
