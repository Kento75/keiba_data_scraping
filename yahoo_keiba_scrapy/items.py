# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class YahooKeibaItem(Item):
    Date = Field()
    Venue = Field()
    Race_no = Field()
    Race_name = Field()
    Surface = Field()
    Distance = Field()
    Order_of_finish = Field()
    Frame_number = Field()
    Horse_numbers = Field()
    Horse_name = Field()
    Age = Field()
    Sex = Field()
    Age = Field()
    Horse_weight = Field()
    D_horse_weight = Field()
    Time = Field()
    Margin = Field()
    Time_3F = Field()
    Jockey_name = Field()
    Load_weight = Field()
    Odds_order = Field()
    Odds = Field()
    Trainer = Field()
    test = Field()
