import urllib.request
import json
import pprint
import time
import at_kick_watch
import at_settle_now
import at_settings

def board2():
    url = 'http://localhost:' + at_settings.port + '/kabusapi/board/' + at_settings.symbol + '@1'
    req = urllib.request.Request(url, method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', at_settings.token)

    try:
        print('###at_board2')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)
            curPrice = content["CurrentPrice"]

            # 現在価格が目標価格に達していたら即決済
            if(curPrice <= at_settings.orderPrice - at_settings.margin):
                at_settle_now.settle_now()
            else:
                #利食い注文(売り発注)
                at_kick_watch.kick_watch()

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import sys
    board2()