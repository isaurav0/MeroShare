from getpass import getpass
import traceback, requests, json
from nature import Dotenv

class MeroShare:

    def __init__(self):
        self.auth_url = 'https://backend.cdsc.com.np/api/meroShare/auth/'
        self.issue_url = 'https://backend.cdsc.com.np/api/meroShare/'\
                         'companyShare/active/search/'
        self.headers = {
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
        self.dotenv = Dotenv()
        self.loginUser()

    def getAuthHeaders(self):
        auth_headers = {
            'Authorization': self.dotenv.get('AUTH'),
            'Content-Length': '446',
        }
        return {**self.headers, **auth_headers}

    def consoleInput(self):
        try:
            username = int(input('Enter username: '))
            password = getpass()
            cid = 174
            return username, password, cid
        except Exception:
            traceback.printexc()

    def getCredentials(self):
        credentials = self.dotenv.get('USERNAME', 'PASSWORD', 'CID')
        if None in credentials:
            self.eraseCredentials()
            credentials = self.consoleInput()
        return credentials

    def eraseCredentials(self):
        self.dotenv.removeAll()

    def loginRequest(self, username, password, cid):
        payload = json.dumps({
            "clientId": cid,
            "username": username,
            "password": password
        })
        res = requests.post(self.auth_url, headers=self.headers, data=payload)
        self.eraseCredentials()
        if res.status_code == 200:
            print('Login successful')
            self.dotenv.set('USERNAME', username)
            self.dotenv.set('PASSWORD', password)
            self.dotenv.set('CID', cid)
            self.dotenv.set('AUTH', res.headers['Authorization'])
            return res.headers['Authorization']
        return None

    def loginUser(self):
        self.auth = self.dotenv.get('AUTH')
        if not self.auth:
            username, password, cid = self.getCredentials()
            self.auth = self.loginRequest(username, password, cid)


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
            self.issue_url,
            headers=self.getAuthHeaders(),
            data=json.dumps(payload)
        )
        if res.status_code == 200:
            return res.text
        else:
            self.dotenv.remove('AUTH')
            print('Please login again.')
            return json.loads(res.text)['message']

    def print_json(self, keys):
        pass
