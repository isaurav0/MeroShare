import sys
import json
import logging
import requests
import datetime
from getpass import getpass
from meroshare.environment import Environment
# from environment import Environment
from prettytable import PrettyTable

class MeroShare:

    def __init__(self, defaultLogin=True):
        self.banks = []
        self.issues = []
        self.application_report = None
        self.company_detail = None
        self.form_detail = None
        self.__auth_url__ = 'https://backend.cdsc.com.np/api/meroShare/auth/'
        self.__issue_url__ = 'https://backend.cdsc.com.np/api/meroShare/'\
                             'companyShare/active/search/'

        self.__application_report_url__ = 'https://backend.cdsc.com.np/api'\
                                          '/meroShare/applicantForm/active'\
                                          '/search/'

        self.__banks_url__ = 'https://backend.cdsc.com.np/api/'\
                             'meroShare/capital/'
        self.__company_share_details_url__ = 'https://backend.cdsc.com.np'\
                                             '/api/meroShare/active/{cid}'

        self.__form_result_url__ = 'https://backend.cdsc.com.np/api/mero'\
                                   'Share/applicantForm/report/detail/{fid}'
        self.__headers__ = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'backend.cdsc.com.np',
            'Origin': 'https://meroshare.cdsc.com.np',
            'Referer': 'https://meroshare.cdsc.com.np/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac'
                          ' OS X 10_15_6) AppleWebKit/537.36 (KHTML'
                          ', like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        self.__env__ = Environment()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        if defaultLogin:
            self.loginUser()

    def pretty_date(self, date):
        return datetime.datetime.strptime(date.split('T')[0],"%Y-%M-%d").strftime("%b %d %Y")

    def __getAuthHeaders__(self, content_length):
        auth = self.__env__.get('AUTH')
        if not auth:
            raise Exception('User Not Authorized')
        auth_headers = {
            'Authorization': auth,
            'Content-Length': str(content_length),
        }
        return {**self.__headers__, **auth_headers}

    def __consoleInput__(self):
        try:
            username = int(input('Enter username: '))
        except Exception:
            raise Exception("InputError: Username Error")

        password = getpass()
        bank_info = input('Enter Bank Full Name or Bank Id: ')
        if bank_info.isnumeric():
            return username, password, int(bank_info)
        else:
            if not bank_info:
                raise Exception("InputError: Bank Info Error.")
            if not self.banks:
                self.getBanks()
            for bank in self.banks:
                if bank['name'].upper() == bank_info.upper():
                    return username, password, int(bank['id'])
            self.printBanks()
            raise Exception("InputError: Input bank info correctly.")

    def __getCredentials__(self):
        credentials = self.__env__.get('USERNAME', 'PASSWORD', 'CID')
        if None in credentials:
            self.eraseCredentials()
            credentials = self.__consoleInput__()
        return credentials

    def __loginRequest__(self, username, password, cid):
        payload = json.dumps({
            "clientId": cid,
            "username": username,
            "password": password
        })
        res = requests.post(self.__auth_url__,
                            headers=self.__headers__,
                            data=payload)
        self.eraseCredentials()
        if res.status_code == 200:
            self.logger.info('Login successful')
            self.__env__.set('USERNAME', username)
            self.__env__.set('PASSWORD', password)
            self.__env__.set('CID', cid)
            self.__env__.set('AUTH', res.headers['Authorization'])
            return res.headers['Authorization']
        print(res.text)
        raise Exception('Incorrect Login Credentials')

    def eraseCredentials(self):
        self.__env__.removeAll()
        self.issues = None
        return self

    def loginUser(self):
        self.auth = self.__env__.get('AUTH')
        if not self.auth:
            username, password, cid = self.__getCredentials__()
            self.auth = self.__loginRequest__(username, password, cid)
        return self

    def logoutUser(self):
        self.__env__.remove('AUTH')
        return self

    def getBanks(self):
        res = requests.get(self.__banks_url__, headers=self.__headers__)
        if res.status_code == 200:
            json_response = json.loads(res.text)
            self.banks = json_response
            return self
        raise Exception(res.text)
        return self

    def printBanks(self):
        if not self.banks:
            raise Exception("FetchError: Use getBanks() first.")
            return
        banks_table = PrettyTable()
        banks_table.field_names = ['Bank Id', 'Bank Name']
        banks_table.vrules = True
        banks_table.hrules = True

        for bank in self.banks:
            banks_table.add_row([bank['id'], bank['name']])
        print(banks_table)

    def getCurrentIssues(self):
        payload = {"filterFieldParams": [
                        {"key": "companyIssue.companyISIN.script","alias":"Scrip"},
                        {"key": "companyIssue.companyISIN.company.name","alias":"Company Name"},
                        {"key": "companyIssue.assignedToClient.name","value":"","alias":"Issue Manager"}
                    ],
                    "page":1,
                    "size":200,
                    "searchRoleViewConstants":"VIEW_OPEN_SHARE",
                    "filterDateParams":[
                        {"key":"minIssueOpenDate","condition":"","alias":"","value":""},
                        {"key":"maxIssueCloseDate","condition":"","alias":"","value":""}
                    ]
                   }
        res = requests.post(
            self.__issue_url__,
            headers=self.__getAuthHeaders__(446),
            data=json.dumps(payload)
        )
        if res.status_code == 200:
            json_response = json.loads(res.text)
            self.issues = json_response['object']
            return self
        self.__env__.remove('AUTH')
        raise Exception('Invalid session: Looks like you logged in from another device.\n Use the same command again.')
        return self

    def printIssues(self):
        if not self.issues:
            self.logger.warning("FetchError: Login again and use getCurrentIssues() first.")
            return

        issues_table = PrettyTable()
        issues_table.field_names = ['CID', 'Company Name', 'Sub Group',
                                    'Share Type', 'Share Group', 'Scrip']
        for issue in self.issues:
            issues_table.add_row([issue['companyShareId'],
                                  issue['companyName'],
                                  issue['subGroup'],
                                  issue['shareTypeName'],
                                  issue['shareGroupName'],
                                  issue['scrip']])
        print(issues_table)

    def getApplicationReport(self):
        payload = {"filterFieldParams":[
                        {"key":"companyShare.companyIssue.companyISIN.script","alias":"Scrip"},
                        {"key":"companyShare.companyIssue.companyISIN.company.name","alias":"Company Name"}
                    ],
                    "page":1,
                    "size":200,
                    "searchRoleViewConstants":"VIEW_APPLICANT_FORM_COMPLETE",
                    "filterDateParams":[
                        {"key":"appliedDate","condition":"","alias":"","value":""},
                        {"key":"appliedDate","condition":"","alias":"","value":""}
                    ]
                }

        res = requests.post(
            self.__application_report_url__,
            headers=self.__getAuthHeaders__(746),
            data=json.dumps(payload)
        )
        if res.status_code == 200:
            json_response = json.loads(res.text)
            self.application_report = json_response['object']
            return self
        self.__env__.remove('AUTH')
        raise Exception('Invalid session: Looks like you logged in from another device.\n Use the same command again.')
        return self

    def printApplicationReport(self):
        if not self.application_report:
            print("FetchError: Application Reports not fetched.")
            return
        report_table = PrettyTable()
        report_table.field_names = ['CID', 'FID', 'Company Name', 'Sub Group',
                                    'Share Type', 'Share Group', 'Scrip']
        for report in self.application_report:
            report_table.add_row([report['companyShareId'],
                                  report['applicantFormId'],
                                  report['companyName'],
                                  report['subGroup'],
                                  report['shareTypeName'],
                                  report['shareGroupName'],
                                  report['scrip']])
        print(report_table)
        return

    def getCompanyDetails(self, cid):
        res = requests.get(
            self.__company_share_details_url__.format(cid=str(cid)),
            headers={**self.__headers__,
                     'Authorization': self.__env__.get('AUTH')
                     }
        )
        if res.status_code == 200:
            json_response = json.loads(res.text)
            self.company_detail = json_response
            return self
        print(res.text)
        self.__env__.remove('AUTH')
        raise Exception('Invalid session: Looks like you logged in from another device.\n Use the same command again.')
        return self

    def printCompanyDetails(self):
        if not self.company_detail:
            print("FetchError: Company Details not fetched. ")

        result = '-------------------------------------------------------\n'
        result += f'Company Name: {self.company_detail["companyName"]}\n'
        result += f'Issue Manager: {self.company_detail["clientName"]}\n'
        result += f'Issue Open Date: {self.pretty_date(self.company_detail["minIssueOpenDate"])}\n'
        result += f'Issue Close Date: {self.pretty_date(self.company_detail["maxIssueCloseDate"])}\n'
        result += f'No. Of Share Issued: {self.company_detail["shareValue"]}\n'
        result += f'Price Per Share: {self.company_detail["sharePerUnit"]}\n'
        result += f'Minimum Quantity: {self.company_detail["minUnit"]}\n'
        result += f'Maximum Quantity: {self.company_detail["maxUnit"]}\n'
        result += f'Sub Group: {self.company_detail["subGroup"]}\n'
        result += f'Share Group Name: {self.company_detail["shareGroupName"]}\n'
        result += f'Share Type: {self.company_detail["shareTypeName"]}\n'
        result += f'Scrip: {self.company_detail["scrip"]}\n'
        result += f'CompanyShareId (cid): {self.company_detail["companyShareId"]}\n'
        result += '-----------------------------------------------------\n'
        print(result)
        return

    def getFormDetails(self, fid):

        res = requests.get(
            self.__form_result_url__.format(fid=str(fid)),
            headers={**self.__headers__,
                     'Authorization': self.__env__.get('AUTH')
                     }
        )

        if res.status_code == 200:
            json_response = json.loads(res.text)
            self.form_detail = json_response
            return self
        self.__env__.remove('AUTH')
        raise Exception('Invalid session: Looks like you logged in from another device.\n Use the same command again.')

    def printFormDetails(self):
        if not self.form_detail:
            print("Form details not available.")
            return self

        result = '-------------------------------------------------------\n'
        result += f'Applied Quantity: {self.form_detail["appliedKitta"]}\n'
        result += f'Applied Amount: {self.form_detail["amount"]}\n'
        result += f'Bank: {self.form_detail["registeredBranchName"]}\n'
        result += f'Account Number: {self.form_detail["accountNumber"]}\n'
        result += f'Application Submitted Date: {self.pretty_date(self.form_detail["appliedDate"])}\n'
        result += f'Status: {self.form_detail["statusName"]}\n'
        result += f'Alloted Amount: {self.form_detail["receivedKitta"]}\n'
        result += f'Remarks: {self.form_detail["meroshareRemark"]}\n'
        result += '-----------------------------------------------------\n'
        print(result)
        return self
