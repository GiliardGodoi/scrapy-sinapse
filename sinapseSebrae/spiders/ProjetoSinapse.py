# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from sinapseSebrae.items import ProjetoItem

from bs4 import BeautifulSoup
import time
import os


class ProjetosinapseSpider(scrapy.Spider):
    name = 'ProjetoSinapse'
    allowed_domains = ['pr1.sinapsedainovacao.com.br']
    start_urls = ['http://pr1.sinapsedainovacao.com.br/']

    def parse(self, response):
        # self.browser = webdriver.Chrome(executable_path='chromedriver.exe')
        self.browser = webdriver.Chrome()
        self.browser.get(response.url)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'list-ideas-inner'))
        WebDriverWait(self.browser, 5).until(element_present)

        lista = self.browser.find_elements_by_css_selector("ul.pagination > li")
        tamanho_lista = len(lista)
        qtd_paginas = lista[tamanho_lista-2].text
        qtd_paginas = int(qtd_paginas)
        print('Quantidade de paginas: ',qtd_paginas)

        URLS = self.get_links(self.browser.page_source,response.url)

        for project_page in URLS:
            yield scrapy.Request(project_page, callback=self.parse_project_page)

        follow_links = getattr(self, 'follow', False)

        if follow_links : 
            qtd_total = getattr(self, 'pages', qtd_paginas)
            qtd_total = int(qtd_total)
            
            for i in range(2,qtd_total):
                time.sleep(5)
                pagination = self.browser.find_element_by_css_selector('ul.pagination')
                caminho = f'//*/a[contains(text(),\'{i}\')]'
                a = pagination.find_element_by_xpath(caminho)
                a.click()
                
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'list-ideas-inner'))
                WebDriverWait(self.browser, 10).until(element_present)
                
                URLS = self.get_links(self.browser.page_source,response.url)
                for project_page in URLS:
                    yield scrapy.Request(project_page, callback=self.parse_project_page)

    def parse_project_page(self,response):
        page = response.url.split("/")[-1]
        filename = 'sinapse-%s.html' % page
        diretorio = os.path.join('data','web',filename)
        with open(diretorio, 'wb') as f:
            f.write(response.body)

        soup = BeautifulSoup(response.body,'html.parser')
        content = soup.find_all("div",{"class":"content"})[0]

        children = content.select("h3, p")
        projeto = ProjetoItem()
        projeto['titulo'] = soup.title.string.strip().strip('.').replace('Sinapse da Inovação -','').strip()
        projeto["url_projeto"] = response.url

        item = children[0]
        if item.get_text().strip() == "Descrição do problema":
            item = children[1]
            projeto['problema'] = item.get_text().strip()
        
        item = children[2]
        if item.get_text().strip() == "Solução Proposta":
            item = children[3]
            projeto["proposta"] = item.get_text().strip('[\n\t]').strip()

        observacoes = list()
        for i in range(4,len(children)):
            item = children[i]
            observacoes.append(item.get_text().strip())

        projeto["observacoes"] = "  ".join(observacoes)

        texto = soup.find('div','well').get_text().strip()
        indice = texto.rfind('em ')
        projeto["atualizacao"] = texto[indice:]

        yield projeto


    def get_links(self,page,url_root):
        list_urls = list()

        soup = BeautifulSoup(page, 'html.parser')        
        div = soup.find_all("div", attrs={"class": "list-ideas-inner"})     

        for p in div:            
            for _, child in enumerate(p.findChildren('a')):                                
                if 'media' in child.get('class',[]):
                    url_idea = url_root + child['href']                                        
                    list_urls.append(url_idea)

        return list_urls
