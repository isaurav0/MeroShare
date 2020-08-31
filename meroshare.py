import json
import requests
import traceback
from getpass import getpass
from environment import Environment

class MeroShare:

    def __init__(self, defaultLogin=True):
        self.__auth_url__ = 'https://backend.cdsc.com.np/api/meroShare/auth/'
        self.__issue_url__ = 'https://backend.cdsc.com.np/api/meroShare/'\
                             'companyShare/active/search/'
        self.__headers__ = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'backend.cdsc.com.np',
            'Origin': 'https://meroshare.cdsc.com.np',
            'Referer': 'https://meroshare.cdsc.com.np/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac'
                          ' OS X 10_15_6) AppleWebKit/537.36 (KHTML'
                          ', like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        self.issues = None
        self.__env__ = Environment()
        if defaultLogin:
            self.loginUser()

    def __getAuthHeaders__(self):
        auth_headers = {
            'Authorization': self.__env__.get('AUTH'),
            'Content-Length': '446',
        }
        return {**self.__headers__, **auth_headers}

    def __consoleInput__(self):
        try:
            username = int(input('Enter username: '))
            password = getpass()
            cid = int(input('Enter cid: '))
            return username, password, cid
        except Exception:
            traceback.printexc()

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
        res = requests.post(self.__auth_url__, headers=self.__headers__, data=payload)
        self.eraseCredentials()
        if res.status_code == 200:
            print('Login successful')
            self.__env__.set('USERNAME', username)
            self.__env__.set('PASSWORD', password)
            self.__env__.set('CID', cid)
            self.__env__.set('AUTH', res.headers['Authorization'])
            return res.headers['Authorization']
        return None

    def eraseCredentials(self):
        self.__env__.removeAll()
        self.issues = None
        return self

    def loginUser(self):
        self.auth = self.__env__.get('AUTH')
        if not self.auth:
            username, password, cid = self.__getCredentials__()
            self.auth = self.__loginRequest__(username, password, cid)

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
            headers=self.__getAuthHeaders__(),
            data=json.dumps(payload)
        )
        if res.status_code == 200:
            self.issues = json.loads(res.text)
            return self
        self.__env__.remove('AUTH')
        print(json.loads(res.text)['message'])
        print('Please start again.')
        return self

    def printIssues(self, keys):
        pass
