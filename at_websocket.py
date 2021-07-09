import sys
import websocket
import _thread
import pprint
import json
import at_settings
import at_cancelorder
import datetime
import urllib.request
import at_board
import time
import printNikkei

def on_message(ws, message):
    printNikkei.printWithTime('--- RECV MSG. --- ')
    #print(message)
    content = json.loads(message)
    pprint.pprint(content)
    curPrice = content["CurrentPrice"]
    pprint.pprint(curPrice)

    if(curPrice >= at_settings.orderPrice + at_settings.lossCutMargin):
        # キャンセルからの損切り注文
        at_settings.lossCutCnt += 1
        at_cancelorder.cancelorder()
        at_settings.isAfterLossCut = True
        ws.close()

def on_error(ws, error):
    if len(error) != 0:
        printNikkei.printWithTime('--- ERROR --- ')
        print(error)

def on_close(ws):
    printNikkei.printWithTime('--- DISCONNECTED --- ')


def on_open(ws):
    printNikkei.printWithTime('--- CONNECTED --- ')
    def run():
        while(True):

            # 指定時間sleep
            time.sleep(at_settings.intervalCloseCheck)

            url = 'http://localhost:' + at_settings.port + '/kabusapi/orders'
            params = { 'product': 0, }
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

                    # 注文情報を取得
                    lastOrder = content[len(content)-1]
                    print(lastOrder['State'])
                            
                    # 全約定の場合(売りが完了している場合)
                    if lastOrder['State'] == 5:

                        # まずはwebsoketを停止
                        printNikkei.printWithTime('closing...')
                        ws.close()
                        break
                    
                    # 手仕舞い時刻
                    nowtime = datetime.datetime.now()
                    if nowtime > at_settings.forceCloseTime:
                        # キャンセルからの損切り注文
                        at_cancelorder.cancelorder()
                        ws.close()
                        break

            except urllib.error.HTTPError as e:
                print(e)
                content = json.loads(e.read())
                pprint.pprint(content)
            except Exception as e:
                print(e)



    _thread.start_new_thread(run, ())

def websocketA1():
    printNikkei.printWithTime('--- websocketA1 Start--- ')
    url = 'ws://localhost:' + at_settings.port + '/kabusapi/websocket'
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

    printNikkei.printWithTime('--- websocketA1 --- ')

    #再エントリチェック
    nowtime = datetime.datetime.now()
    
    if nowtime < at_settings.stopOrderTime:
        # ロスカットは1回以上したら終了
        if at_settings.lossCutCnt < 1:
            # 指定時間sleep後再び買い発注
            if at_settings.isAfterLossCut:
                at_settings.isAfterLossCut = False
                time.sleep(at_settings.intervalAfterLossCut)
            else:
                time.sleep(at_settings.intervalOrders)

            #念のためもろもろ変数初期化
            at_settings.orderPrice = 0
            at_settings.orderID = ""

            #再エントリ            
            at_board.board()


if __name__ == "__main__":
    import sys
    websocketA1()
