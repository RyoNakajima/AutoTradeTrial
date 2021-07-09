import urllib.request
import json
import pprint
import at_board2
import at_settings

def orders_info():
    url = 'http://localhost:' + at_settings.port + '/kabusapi/orders'
    params = { 'product': 0, }
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', at_settings.token)

    try:
        print('###at_order_info')
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            pprint.pprint(content)

            # 注文情報を取得
            firstOrder = content[len(content)-1]
            print(firstOrder['Details'])
            firstOrderDetails = firstOrder['Details']
            firstDetailOrder = firstOrderDetails[len(firstOrderDetails)-1]
            at_settings.orderPrice = firstDetailOrder['Price']


            #注文銘柄の現在価格を調査(即決済の可能性ため)
            at_board2.board2()

    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import sys
    orders_info()