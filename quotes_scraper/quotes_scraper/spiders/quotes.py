# Lo primero a hacer es importar el módulo de scrapy.
import scrapy

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
    # En este caso a modo de demostración imprimiremos el status de la respuesta y sus headers
        print('*' * 10)
        print('\n\n')
        print(response.status, response.headers)
        print('*' * 10)
        print('\n\n')
