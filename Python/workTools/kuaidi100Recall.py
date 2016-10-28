import requests
import argparse
import json
from pprint import pprint
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Update Express Tracking Info')
parser.add_argument('-u', '--user', help='login user name')
parser.add_argument('-p', '--password', help='login password')
parser.add_argument('-f', '--file', help='Express Json File Path')
args = parser.parse_args()
print '\033[1;36;40m'
print r'''
 _____ ___   ___  _     _  _______ _____
|_   _/ _ \ / _ \| |   | |/ / ____|_   _|
  | || | | | | | | |   | ' /|  _|   | |
  | || |_| | |_| | |___| . \| |___  | |
  |_| \___/ \___/|_____|_|\_\_____| |_|
 _____                                _____               _    _
| ____|_  ___ __  _ __ ___  ___ ___  |_   _| __ __ _  ___| | _(_)_ __   __ _
|  _| \ \/ / '_ \| '__/ _ \/ __/ __|   | || '__/ _` |/ __| |/ / | '_ \ / _` |
| |___ >  <| |_) | | |  __/\__ \__ \   | || | | (_| | (__|   <| | | | | (_| |
|_____/_/\_\ .__/|_|  \___||___/___/   |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
           |_|                                                         |___/
'''
if args.user is None or args.password is None or args.file is None:
    print '\033[1;31;40m'
    print 'You Must Input username, password, filepath'
    exit()
s = requests.session()
login_url = 'http://www.kuaidi100.com/pollquery/login.do'
login = s.post(login_url, {'name': args.user, 'password': args.password})
expresses = json.load(file(args.file))
url = 'http://www.kuaidi100.com/polltest/testapi.do'
ending = {'success': 0, 'fail': 0}
for express in tqdm(expresses):
    post_data = {
        'method': 'normal',
        'schema': 'json',
        'company': express['company'],
        'resultv2': 0,
        'code': express['code']
    }
    req = s.post(url, post_data)
    result = json.loads(req.content)
    if result['result']:
        callback = {
            'method': 'send',
            'data': result['message'],
            'url': 'http://lenovomobileservice.com/mgs/index.php//kuaidiCallBack/kd'
        }
        callback_req = s.post(url, callback)
        callback_res = json.loads(callback_req.content)
        if callback_res['result']:
            ending['success'] += 1
        else:
            print callback_res['message']
            ending['fail'] += 1
    else:
        ending['fail'] += 1

print '\033[1;32;40m'
print 'Update Tracking Success: {}'.format(ending['success'])
print '\033[1;31;40m'
print 'Update Tracking Fail: {}'.format(ending['fail'])
