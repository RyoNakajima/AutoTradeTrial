import urllib.request
import json
import pprint
import time
import at_settle_now
import at_settings

def cancelorder():
    obj = { 'OrderID': at_settings.orderID, 'Password': at_settings.password }
    json_data = json.dumps(obj).encode('utf8')

    url = 'http://localhost:' + at_settings.port + '/kabusapi/cancelorder'
    req = urllib.request.Request(url, json_data, method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', at_settings.token)

    try:
        print('###rsi1570i_cancelorder')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            #約定するまで1分待つ
            time.sleep(at_settings.intervalAfterOrder)

            at_settle_now.settle_now()


    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import sys
    cancelorder()