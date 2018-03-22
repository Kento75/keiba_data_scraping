# keiba_data_scrapy

yahoo競馬のレース結果を取得するスクレイピングツール

keiba_url_getter」リポジトリで作成したCSVを元にスクレイピングを行う。

レースに出走した馬のデータを取得し、CSV形式のファイルを生成する。

*****
#### 動作確認済み構成

OS    ：Ubuntu16.0.4 LTS 64bit

python：Python3.5.3、Python3.6.3

CPU   ：core i3 540

RAM   ：8GB

LAN   ：有線

※ 競馬データを全件取得する場合、処理を完了するのに７日以上かかり
 　RAMを圧迫するので、8GBは必須。

*****
#### 環境構築

pipコマンドを使用して下記コマンドを実行
　pip install -r requirements.txt

cloneしたプロジェクト内に移動
　cd keiba_data_scrapy
 
プロジェクト内のCSVディレクトリに「url_list.csv」を配置

cloneしたプロジェクト内に移動後、下記コマンドを実行
　scrapy crawl yahoo_keiba

*****
#### todo

取得したデータにタイムが1分以上のデータがあり、DBへのint型への取り込みができない不具合の対応
コードが汚いのでいつか修正する...

*****
#### 修正済み

2018/3/23  距離カラムの追加
