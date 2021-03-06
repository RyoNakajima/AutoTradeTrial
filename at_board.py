import urllib.request
import json
import pprint
import time
import pandas as pd
import numpy as np
import at_settings
import sqlite3
from statistics import mean 
import datetime
import at_sendorder_entry

def board():
    url = 'http://localhost:' + at_settings.port + '/kabusapi/board/' + at_settings.symbol + '@1'
    req = urllib.request.Request(url, method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', at_settings.token)

    curPriceList = []

    #標準偏差初期化
    std_val = 0
    #閾値越えフラグを初期化
    threshold_over = False

    while True:
        try:
            print('###at_board')
            with urllib.request.urlopen(req) as res:
                print(res.status, res.reason)
                for header in res.getheaders():
                    print(header)
                print()
                content = json.loads(res.read())
                pprint.pprint(content)
                curPrice = content["CurrentPrice"]
                if curPrice is None:
                    #現在値が取れない場合はまだ相場が開いてないのでスキップ
                    continue
                
                curPriceList.append(curPrice)
                print("curPrice", end = ":")
                print(curPrice)

                #標準偏差用
                list_for_std = curPriceList.copy()

                if len(curPriceList) > 20:
                    del curPriceList[0:len(curPriceList)-20]
                    print("curPrice after del", end = ":")
                    print(curPrice)

                if len(list_for_std) > 20:
                    del list_for_std[0:len(list_for_std)-20]
                    print("list_for_std after del", end = ":")
                    print(list_for_std)

                    #1つ前の標準偏差値を退避
                    pre_std_val = std_val
                    #標準偏差を求める
                    std_val = np.std(list_for_std)
                    print("std_val", end = ":")
                    print(std_val)

                    #RSIを求める
                    delta_list = np.diff(curPriceList)
                    print("delta_list", end = ":")
                    print(delta_list)
                    up_list, down_list = delta_list.copy(), delta_list.copy()
                    print("up_list", end = ":")
                    print(up_list)
                    print("down_list", end = ":")
                    print(down_list)
                    up_list[up_list < 0] = 0
                    print("up_list after edit", end = ":")
                    print(up_list)
                    down_list[down_list > 0] = 0
                    print("down_list after edit", end = ":")
                    print(down_list)
                    up_list_mean = up_list.mean()
                    print("up_list_mean", end = ":")
                    print(up_list_mean)
                    down_list_mean = down_list.mean()
                    print("down_list_mean", end = ":")
                    print(down_list_mean)
                    rsi =  up_list_mean / (up_list_mean + abs(down_list_mean)) * 100
                    print("rsi", end = ":")
                    print(rsi)

                    #標準偏差が閾値を超えたらフラグを立てる
                    if rsi > at_settings.rsi_threshold and std_val > at_settings.sd_threshold:
                        threshold_over = True
                    
                    #標準偏差が閾値を超えたのち、標準偏差が減少傾向になったらエントリ
                    if threshold_over and pre_std_val > std_val:
                        # 指定時間を超えていたらエントリしない
                        nowtime = datetime.datetime.now()
                        if nowtime > at_settings.morningStartTime and nowtime < at_settings.stopOrderTime:
                            at_sendorder_entry.sendorder_entry()

                        break
                        

        except urllib.error.HTTPError as e:
            print(e)
            content = json.loads(e.read())
            pprint.pprint(content)
        except Exception as e:
            print(e)
        time.sleep(60)

if __name__ == "__main__":
    import sys
    board()