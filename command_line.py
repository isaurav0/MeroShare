#! /usr/local/bin/python3
import sys
from meroshare import MeroShare

help_message='''

    A command line tool to get meroshare details

    Usage: meroshare [option] [optional_options]

    Viewing banks
        -> meroshare banks

    Logging in
        -> meroshare login

        requires username, password and bank_id or bank_name
        bank details can be found from [banks] switch

    Viewing current issues
        -> meroshare current_issues

    Viewing submitted applications
        -> meroshare reports

    Viewing company details
        -> meroshare company [company_id]
        [company_id] can be found from issues and reports

    Logging out
        -> meroshare logout

'''

def main():

    if len(sys.argv) < 2:
        print(help_message)
        exit()

    option = sys.argv[1]

    if option == 'banks':
        share = MeroShare(defaultLogin=False)
        share.getBanks().printBanks()
        return

    share = MeroShare(defaultLogin=True)

    if option == 'login':
        pass

    elif option == 'current_issues':
        share.getCurrentIssues().printIssues()

    elif option == 'reports':
        share.getApplicationReport().printApplicationReport()

    elif option == 'company':
        if len(sys.argv) < 3:
            print(help_message)
            exit()

        cid = sys.argv[2]
        share.getCompanyDetails(cid).printCompanyDetails()

    elif option == 'logout':
        share.eraseCredentials()
        print('Logged Out.')

    else:
        print(help_message)
        exit()

if __name__ == '__main__':
    main()
