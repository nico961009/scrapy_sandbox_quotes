# Lo primero a hacer es importar el módulo de scrapy.
import scrapy


# Se colocan las rutas XPath de cada elemento comentado
# Título = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags= //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()

# Definimos nuestra clase que deberá heredar de scrapy a Spider.
class QuotesSpider(scrapy.Spider):
    #La clase tiene tres paramétros fundamentales:
    # El primero es el nombre por el cual nos reeferiremos a este spider
    # este nombre no se puede repetir en el futuro.
    name = 'quotes'

    # El segundo es una lista de url´s que contendrá todas las listas de url´s a las cuales
    # nosotros vamos a scrappear (a estas direcciones les haremos la petición http):
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    # El tercero es definir un método llamado parse (esto es analizar un archivo para extraer
    # información valiosa a partir de este) para analizar la respuesta del request. Este método 
    # tiene dos argumentos, el primero es "self" por ser un método de una clase y el argumento:
    # "response" que es la respuesta http a la url listada arriba.
    def parse(self, response):
        
        print('*' * 10)
        print('\n\n\n')

        # Se define una variable para extraer el título de nuestra página
        # a scrappear. No olvides el método get() para hacer la extracción.
        title = response.xpath('//h1/a/text()').get()
        print(f'Titulo: {title}')
        print('\n\n')

        # En este caso al tratarse da varias citas se aplica el método .getall().
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        print('Citas: ')
        # Al ser varias citas es necesario hacer un for:
        for quote in quotes:
            print(f'- {quote}')
        print('\n\n')

        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        print('Top Ten Tags: ')
        # Al ser varias citas es necesario hacer un for:
        for tag in top_ten_tags:
            print(f'- {tag}')
        print('\n\n')

        print('\n\n\n')
        print('*' * 10)
        
