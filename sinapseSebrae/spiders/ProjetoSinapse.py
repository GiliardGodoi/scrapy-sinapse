# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
import bs4
from time import sleep
from os import path
from re import split as re_split


class ProjetoSinapseSpider(scrapy.Spider):
    name = 'ProjetoSinapse'
    allowed_domains = ['pr1.sinapsedainovacao.com.br']
    start_urls = ['http://pr1.sinapsedainovacao.com.br/']

    def closed(self, reason):
        
        if self.browser:
            self.browser.close()
            self.browser.quit()
            self.browser = None

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
                sleep(5)
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
        diretorio = path.join('data','web',filename)
        with open(diretorio, 'wb') as f:
            f.write(response.body)

        soup = BeautifulSoup(response.body,'html.parser',from_encoding="utf-8")
        
        projeto = dict()
        projeto["url_projeto"] = response.url

        projeto.update(get_data_from_div_media_body(soup))
        projeto.update(get_data_from_div_content(soup))
        projeto.update(get_data_from_div_sidebar(soup))

        texto = soup.find('div','well').get_text().strip()
        indice = texto.rfind('em ')
        projeto["atualizado"] = texto[indice:]

        yield projeto


    def get_links(self,page,url_root):
        list_urls = list()

        soup = BeautifulSoup(page, 'html.parser')        
        div = soup.find_all("div", attrs={"class": "list-ideas-inner"})     

        for p in div:            
            for _, child in enumerate(p.findChildren('a')):                                
                if 'media' in child.get('class','-'):
                    url_idea = url_root + child['href']                                        
                    list_urls.append(url_idea)

        return list_urls


def get_data_from_div_media_body(soup):
    data = dict()
    data.setdefault('comentarios','0')
    data.setdefault('favoritos','0')
    div = soup.find('div',attrs={'class' : 'media-body'})
    data['titulo'] = div.h1.string
    data['categoria'] = div.a.string

    for element in div.find_all('span'):
        if isinstance(element,bs4.element.Tag):
                if element.string == 'Setores:':
                    tmp = element.next_sibling.strip('[\n\t ]+')
                    data['setor'] = tmp.split('/')
                elif element.string == 'Região':
                    data['regiao'] = element.next_sibling.strip('[\n\t ]+')
                elif element.get('title') == 'Favoritada':
                    if element.text.strip():
                        data['favoritos'] = element.text.strip()

    link = div.find('a',attrs={'class': 'count'})
    if link.text.strip():
        data['comentarios'] = link.text.strip()

    return data

def get_data_from_div_content(soup):
    data = dict()
    div = soup.find('div',attrs={'class':'content'})
    children = div.select('h3, p')

    schema = {
        'Descrição do problema' : 'problema',
        'Solução Proposta' : 'proposta',
        'Estágio de desenvolvimento' : 'estagio',
        'Diferenciais da Solução' : 'diferencial',
        'Políticas públicas' : 'politicas'
    }
    for e in children:
        if e.name == 'h3':
            key = schema.get(e.string.strip(),'outros')
        elif e.name == 'p':
            if data.get(key,False):
                ## key already exists
                data[key] += e.text.strip('[\n\t ]+')
            else :
                ## key não existe previamente
                data[key] = e.text.strip('[\n\t ]+')

    return data


def get_data_from_div_sidebar(soup):
    data = dict()

    div = soup.find('div',attrs={'class':'sidebar'})
    text = div.text.strip('[\n\t ]+')
    texts = re_split('[\n\t]+',text)
    sobre, cidade, nome, *resto = texts
    del sobre

    data['cidade'] = cidade.replace('Cidade:','').strip()
    data['nome'] = nome
    resto = ' '.join(resto)
    resto = resto.replace('pt_BR','').replace('Compartilhe essa Ideia','').replace('Tweetar','').strip()
    data['sobre'] = resto

    return data





