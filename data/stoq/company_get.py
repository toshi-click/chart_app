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

import datetime

import pandas as pd
import pandas_datareader.data as web
# Google Drive認証
from google.colab import drive

# /content/drive/My Drive/xx/xx/
drive.mount('/content/drive')

# JPXの東証上場一覧のページへのアクセス
!wget 'https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls' -O data_j.xls -a wget-log

## pandasでexcelファイルの読み込みとdf整形など
df = pd.read_excel("data_j.xls")
df.columns = ['date', 'code', 'name', 'lst', 'sectorCode', 'sectorName', 'flr1', 'flr2', 'flr3', 'flr4']
drop_col = ['flr1', 'flr2', 'flr3', 'flr4']
df = df.drop(drop_col, axis=1)  # 不要な列の削除

## dfのグルーピングとグループ指定(1グループ240銘柄に限定する)
j = 0
for index, item in df.iterrows():
    if j <= index / (len(df) / 20) < j + 1:
        ### 中身を文字型に変換して'.JP'を付与

        code = str(item['code']) + '.JP'

        df1 = web.DataReader(code, "stooq")

        df1['Code'] = item['code']

        # csv保存：listed_yyyymmdd_j.csv
        now = datetime.datetime.now()
        yyyymmdd = now.strftime("%Y%m%d")
        filename = "/content/drive/My Drive/stooq/listed_" + str(yyyymmdd) + "_" + str(item['code']) + ".csv"
        df1.to_csv(filename, encoding="utf-8")
        print(str(item['code']) + 'saved_csv finish!')

print('All_finish!')
