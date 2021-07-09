import urllib.request
import json
import pprint
import at_websocket
import time
import at_settings

def kick_watch():
    # まずは利食い注文
    obj = { 'Password': at_settings.password,
            'Symbol': at_settings.symbol,
            'Exchange': 1,
            'SecurityType': 1,
            'Side': '2',
            'CashMargin': 3,
            'MarginTradeType': 1,
            'DelivType': 2,
            'AccountType': 4,
            'Qty': at_settings.qty,
            'ClosePositionOrder': 0,
            'Price': at_settings.orderPrice - at_settings.margin,
            'ExpireDay': 0,
            'FrontOrderType': 20}
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + at_settings.port + '/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', at_settings.token)

    try:
        print('###at_kick_watch:' + at_settings.port + ':' + str(at_settings.orderPrice))
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            #損切り監視用の注文IDを保存
            at_settings.orderID = content['OrderId']
            pprint.pprint(at_settings.orderID)

            #損切り用値監視
            at_websocket.websocketA1()
            
    except urllib.error.HTTPError as e:
        print('###kabusapi_sendorder2:HTTPError')
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print('###kabusapi_sendorder2:Exception')
        print(e)
        
if __name__ == "__main__":
    import sys
    kick_watch()