import urllib.request
import json
import pprint
import at_settings

# url = 'http://localhost:18080/kabusapi/ranking' #?type=1&ExchangeDivision=ALL
url = 'http://localhost:' + at_settings.port + '/kabusapi/ranking'

params = { 'type': 1 } #type - 1:値上がり率（デフォルト）2:値下がり率 3:売買高上位 4:売買代金 5:TICK回数 6:売買高急増 7:売買代金急増 8:信用売残増 9:信用売残減 10:信用買残増 11:信用買残減 12:信用高倍率 13:信用低倍率 14:業種別値上がり率 15:業種別値下がり率
params['ExchangeDivision'] = 'T' #ExchangeDivision - ALL:全市場（デフォルト）T:東証全体 T1:東証一部 T2:東証二部 TM:マザーズ JQ:JASDAQ M:名証 FK:福証 S:札証
req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method='GET')
req.add_header('Content-Type', 'application/json')
req.add_header('X-API-KEY', at_settings.token)

try:
    with urllib.request.urlopen(req) as res:
        print(res.status, res.reason)
        for header in res.getheaders():
            print(header)
        print()
        content = json.loads(res.read())
        pprint.pprint(content)
except urllib.error.HTTPError as e:
    print(e)
    content = json.loads(e.read())
    pprint.pprint(content)
except Exception as e:
    print(e)
