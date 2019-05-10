# Scrapy Sinapse da Inovação

Analisando os projetos de inovação inscritos na Plataforma Sinapse da Inovação <pr1.sinapsedainovacao.com.br>.

Este projeto utilizao *framework Scrapy* e *Selenium* para realizar a captura das informações do projeto. Certifique-se que possui as dependências instaladas.

## Configurando Ambiente

O arquivo para com as depêndencias necessárias, foi criado da seguinte forma:

```python
conda env export > <environment-name>.yml
activate <environment-name>
```

O ambiente pode ser criado da seguinte forma

```python
conda env create -f <environment-name>.yml
```

Também é necessário possuir a extensão *chromedriver* para o Selenium incluido no PATH do sistema operacional. <Não consegui fazer de forma diferente>.

A extensão pode ser obtida neste site <http://chromedriver.chromium.org/downloads>

### Para adicionar variáveis de ambiente no Windows

Siga estes procedimentos:
- No explorer clique no item 'Meu Computador' com o botão direito do mouse;
- Escolhas as opções 'Propriedades' > 'Configurações avançadas do sistema' > 'Variáveis de ambiente'
- Selecione a variável 'Path' e selecione a opção 'Editar'
- Selecione 'Novo' e inclua o caminho até a pasta que contém o drive.

## Como o projeto foi gerado

Estes comandos não precisam ser executados, mas é bom saber.

```python
scrapy startproject sinapseSebrae
```

O Spider para o site foi gerado a partir do comando

```python
scrapy genspider ProjetoSinapse pr1.sinapsedainovacao.com.br
```

## Executando o projeto

Executar o projeto utilize o comando abaixo. 'ProjetoSinapse' é o nome do spider definido na classe ProjetoSinapse em *spiders*.

```python
scrapy crawl ProjetoSinapse
```

Personalizando parâmetros:

```python
scrapy crawl ProjetoSinapse -o projetos.json -a follow=True -a pages=3 --logfile output.log
```

## Referências

[Web Scraping Reference: A Simple Cheat Sheet for Web Scraping with Python](https://blog.hartleybrody.com/web-scraping-cheat-sheet/) por Hartley Brody. Acessado em 09/05/2019.

[Beautiful Soup 4 Cheatsheet](http://akul.me/blog/2016/beautifulsoup-cheatsheet/). Acessado em 09/05/2019.

[W3Schools Css Selectors](https://www.w3schools.com/cssref/css_selectors.asp). Acessado em 09/05/2019.

[Scrapy's Framework Documentation](https://docs.scrapy.org/en/latest/index.html). Acessado em 09/05/2019.

## Agradecimentos
