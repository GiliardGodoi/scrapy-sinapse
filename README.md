# Scrapy Sinapse da Inovação

Analisando os projetos de inovação inscritos na Plataforma Sinapse da Inovação <pr1.sinapsedainovacao.com.br>.

Este projeto utilizao *framework Scrapy* e *Selenium* para realizar a captura das informações do projeto. Certifique-se que possui as dependências instaladas.

## Configurando Ambiente

O arquivo para criar o ambiente com as depêndencias necessárias foram criadas da seguinte forma.

```python
conda env export > <environment-name>.yml
activate <environment-name>
```

O ambiente pode ser criado da seguinte forma

```python
conda env create -f <environment-name>.yml
```

Para rodar o projeto é necessário possuir a extensão *chromedriver* para o Selenium incluido no PATH do sistema operacional. <Não consegui fazer de forma diferente>.

A extensão pode ser obtida neste site <http://chromedriver.chromium.org/downloads>

### Para adicionar variáveis de ambiente no Windows

Siga estes procedimentos:

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

´´´python
scrapy crawl ProjetoSinapse
´´´

Personalizando parâmetros
´´´python
scrapy crawl quotes -o quotes-humor.json -a tag=humor
´´´

## Referências

[Web Scraping Reference: A Simple Cheat Sheet for Web Scraping with Python](https://blog.hartleybrody.com/web-scraping-cheat-sheet/) por Hartley Brody. Acessado em 09/05/2019.
[Beautiful Soup 4 Cheatsheet](http://akul.me/blog/2016/beautifulsoup-cheatsheet/)
[W3Schools Css Selectors](https://www.w3schools.com/cssref/css_selectors.asp)
[Scrapy's Framework Documentation](https://docs.scrapy.org/en/latest/index.html)

## Agradecimento