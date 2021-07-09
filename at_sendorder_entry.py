import urllib.request
import json
import pprint
import at_order_info
import time
import at_settings

def sendorder_entry():
    print('###at_sendorder_entry -START-')
    obj = { 'Password': at_settings.password,
            'Symbol': at_settings.symbol,
            'Exchange': 1,
            'SecurityType': 1,
            'Side': at_settings.side,
            'CashMargin': 2,
            'MarginTradeType': 1,
            'DelivType': 0,
            'AccountType': 4,
            'Qty': at_settings.qty,
            'ClosePositionOrder': 0,
            'Price': 0,
            'ExpireDay': 0,
            'FrontOrderType': 10}
    json_data = json.dumps(obj).encode('utf-8')

    url = 'http://localhost:' + at_settings.port + '/kabusapi/sendorder'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', at_settings.token)

    try:
        print('###rsi1570_sendorder_entry')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            #約定するまで1分待つ
            time.sleep(at_settings.intervalAfterOrder)

            # 約定した価格を調査する
            at_order_info.orders_info()

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import sys
    sendorder_entry()