# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ProjetoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titulo = scrapy.Field()
    problema = scrapy.Field()
    proposta = scrapy.Field()
    observacoes = scrapy.Field()
    # equipe = scrapy.Field()
    atualizacao = scrapy.Field()
    url_projeto = scrapy.Field()
