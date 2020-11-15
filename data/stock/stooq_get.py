# Google colaboratory
#事前処理
#!pip list
!pip install -q xlrd
!pip install pandas_datareader

###############################################
# Jupyter_notebook's Shortcut
# Ctrl + \ :すべてのランタイムをリセット[←ショートカットを任意に割り振り]
# Ctrl + Enter :セルを実行
###############################################

from google.colab import files

import google.colab
import googleapiclient.discovery
import googleapiclient.http

import time
import sys
import pandas as pd
import pandas_datareader.data as web
# Google Drive認証
from google.colab import drive

# /content/drive/My Drive/xx/xx/
drive.mount('/content/drive')

# JPXの東証上場一覧のページへのアクセス
!wget 'https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls' -O data_j.xls -a wget-log

## pandasでexcelファイルの読み込みとdf整形など
company_df = pd.read_excel("data_j.xls")
company_df.columns = ['date', 'code', 'name', 'lst', 'sectorCode', 'sectorName', 'flr1', 'flr2', 'flr3', 'flr4']
drop_col = ['flr1', 'flr2', 'flr3', 'flr4']
company_df = company_df.drop(drop_col, axis=1)  # 不要な列の削除

## j=0～19 で一度にアクセスしすぎないようにする
j = 0
# j = 1
# j = 2
# j = 3
# j = 4
# j = 5
# j = 6
# j = 7
# j = 8
# j = 9
# j = 10
# j = 11
# j = 12
# j = 13
# j = 14
# j = 15
# j = 16
# j = 17
# j = 18
# j = 19
count = 0
tmp_code = 0
for index, item in company_df.iterrows():
    if j <= index / (len(company_df) / 20) < j + 1:
        if count == 0:
            print('from:'+str(item['code'])+' start!')
            count = 1
        ### 中身を文字型に変換して'.JP'を付与
        code = str(item['code']) + '.JP'
        stock_df = web.DataReader(code, "stooq")
        # 早すぎると規制されるっぽいのでsleep
        time.sleep(1)

        # 1日の制限超えた応答きたらエラー終了させる
        if stock_df.empty:
            print('error:' + str(item['code']) + ' daily over!')
            sys.exit(1)

        stock_df['Code'] = item['code']

        # 後処理のために明示的にカラムを並び替える
        stock_df.reindex(columns=['Code', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

        # csv保存：[stock_code].csv
        filename = "/content/drive/My Drive/stock/" + str(item['code']) + ".csv"
        stock_df.to_csv(filename, encoding="utf-8")
        tmp_code = item['code']

print('to:'+str(tmp_code)+' end!')
print('All_finish!')
