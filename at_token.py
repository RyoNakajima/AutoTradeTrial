import urllib.request
import json
import pprint
#import sys
import at_register
import at_settings

obj = { 'APIPassword': at_settings.apiPassword }
json_data = json.dumps(obj).encode('utf8')

url = 'http://localhost:' + at_settings.port + '/kabusapi/token'

req = urllib.request.Request(url, json_data, method='POST')
req.add_header('Content-Type', 'application/json')

try:
    print('###at_token')
    with urllib.request.urlopen(req) as res:
        print(res.status, res.reason)
        for header in res.getheaders():
            print(header)
        print()
        content = json.loads(res.read())
        pprint.pprint(content)
        token = content["Token"]
        at_settings.token = token
        #PUSh配信銘柄登録
        at_register.register()
except urllib.error.HTTPError as e:
    print(e)
    content = json.loads(e.read())
    pprint.pprint(content)
except Exception as e:
    print(e)
