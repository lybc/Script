import requests

for i in range(3278, 3405):
    url = 'baseurl/changes/{}/abandon'.format(i)
    print url
    headers = {
        'Cookie': 'your cookie',
        'x-Gerrit-Auth': 'aGKu.QkqNdmSgwl.Szs2sL10FSeGwTS'
    }
    r = requests.post(url, headers=headers)
    print r.content