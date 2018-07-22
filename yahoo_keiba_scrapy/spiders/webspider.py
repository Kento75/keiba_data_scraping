import re
import pandas as pd
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from yahoo_keiba_scrapy.items import YahooKeibaItem


class PredictSpider(CrawlSpider):
    # yahoo_keibaはSpiderの名前。spiderの実行時に入力する。
    name = 'yahoo_keiba'

    allowed_domains = ['keiba.yahoo.co.jp']

    start_urls = []

    def __init__(self, *args, **kwargs):
        super(PredictSpider, self).__init__(*args, **kwargs)

        df = pd.read_csv('./csv/url_list.csv', header=None)
        self.start_urls = df[3]

    # サーバー負荷を考慮してスクレイピング間隔の調整
    # 5秒に一度リクエスト送信
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
    }

    # 再帰的にページのリンクを取得
    rules = [
        # 正規表現にマッチするリンクをparseメソッドでスクレイピング
        Rule(LinkExtractor(), callback='parse'),
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        # テーブルヘッダをすべて取得
        divs = hxs.select('/html/body/div[2]/div[1]/div[1]/table[2]/tbody/tr')
        # 開催日
        date_d = re.sub(r'\/$', '', re.sub(r'月|火|水|木|金|土|日', '', re.sub(r'（|）|\s|日', '', re.sub(r'年|月', '/', hxs.select('//*[ @ id = "raceTitDay"]/text()').extract()[0]))))
        # 開催地
        venue_d = re.sub(r'[0-9]{1,2}回|[0-9]{1,3}日|\s', '', hxs.select('//*[ @ id = "raceTitDay"]/text()').extract()[1])
        # レース番号
        race_no_d = re.sub(r'\n|[^0-9]|\s', '', hxs.select('// *[ @ id = "raceNo"]/text()').extract_first())
        # レース名
        race_name_d = re.sub(r'\s.*', '', hxs.select('/html/head/meta[7]/@content')[0].extract())
        # コース種別(ダート、芝)
        surface_d = re.sub(r' +', '', re.sub(r'・.*', '', hxs.select('//*[@id="raceTitMeta"]/text()').extract_first()))
        # 距離
        distance_d = re.sub(r'\n|[^0-9]|\s', '', hxs.select('//*[@id="raceTitMeta"]/text()').extract_first())

        # テーブルヘッダを一ずつ取得してテーブルデータをitemに保存する
        for div in divs:
            item = YahooKeibaItem()
            # 開催日
            item['Date'] = date_d
            # 開催地
            item['Venue'] = venue_d
            # レース馬号
            item['Race_no'] = race_no_d
            # レース名
            item['Race_name'] = race_name_d
            # コース種別(ダート、芝)
            item['Surface'] = surface_d
            # 距離
            item['Distance'] = distance_d
            # 着順
            ch_order_of_finish = re.sub(r'\n|\s', '', div.select('./td[1]/text()').extract()[0])
            item['Order_of_finish'] = ch_order_of_finish
            # 枠番
            item['Frame_number'] = re.sub(r'\n|\s', '', div.select('./td[2]/span/text()').extract()[0])
            # 馬番
            item['Horse_numbers'] = re.sub(r'\n|\s', '', div.select('./td[3]/text()').extract()[0])
            # 馬名
            item['Horse_name'] = div.select('./td[4]/a/text()').extract()[0]
            # 性別
            item['Sex'] = re.sub(r'[0-9a-zA-Z]|\n', '', re.sub(r'\/.*', '', div.select('./td[4]/span/text()').extract()[0]))
            # 年齢
            item['Age'] = re.sub(r'[^0-9]', '', re.sub(r'\/.*', '', div.select('./td[4]/span/text()').extract()[0]))
            # 馬体重
            ch_horse_weight = re.sub(r'\s-\s', '', re.sub(r'\(.*', '', re.sub(r'\n[^0-9a-zA-Z]{1,2}[0-9]{1,2}\/', '', div.select('./td[4]/span/text()').extract()[0])))

            if ch_horse_weight is '-':
                item['Horse_weight'] = '0'
            else:
                item['Horse_weight'] = ch_horse_weight

            # 体重増減
            ch_d_horse_weight = re.sub(r'\s-\s', '', re.sub(r'[^0-9\-]', '', re.sub(r'\n.*\(', '', div.select('./td[4]/span/text()').extract()[0])))
            if ch_d_horse_weight in '-':
                item['D_horse_weight'] = 0
            else:
                item['D_horse_weight'] = ch_d_horse_weight

            # タイム
            ch_time = re.sub(r'\n', '', div.select('./td[5]/text()').extract()[0])
            if len(ch_time) >= 6:
                item['Time'] = float(ch_time[2:]) + 60
            else:
                item['Time'] = ch_time

            # 着差
            if div.select('./td[5]/span/text()').extract_first() is not None:
                item['Margin'] = re.sub(r'\s|\(|\)', '', div.select('./td[5]/span/text()').extract()[0])
            else:
                item['Margin'] = ''

            # 上り3F
            ch_time_3f = re.sub(r'[^0-9\.]', '', div.select('./td[6]/span/text()').extract()[0])

            if len(ch_time_3f) >= 6:
                item['Time_3f'] = float(ch_time_3f[2:]) + 60
            else:
                item['Time_3F'] = ch_time_3f

            # 騎手
            item['Jockey_name'] = div.select('./td[7]/a/text()').extract()[0]
            # 騎手重量
            item['Load_weight'] = re.sub(r'[^0-9\.]', '', div.select('./td[7]/span/text()').extract()[0])
            # 人気
            item['Odds_order'] = re.sub(r'\s|\n', '', div.select('./td[8]/text()').extract()[0])
            # オッズ
            if div.select('./td[8]/span/text()').extract_first() is not None:
                item['Odds'] = re.sub(r'\s|\(|\)', '', div.select('./td[8]/span/text()').extract()[0])
            else:
                # ない場合もあるので人気を入れる
                item['Odds'] = re.sub(r'\s|\n', '', div.select('./td[8]/text()').extract()[0])

            # 調教師
            item['Trainer'] = div.select('./td[9]/a/text()').extract()[0]
            yield item
