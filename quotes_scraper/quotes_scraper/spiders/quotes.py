import scrapy

# Título = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags= //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button=//ul[@class="pager"]//li[@class="next"]/a/@href


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    # Generamos un atributo de configuración para automátizar algunos procesos como el guardar
    # el output en un archivo .json:
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
    }

    # creamos un nuevo método tipo parse para extraer únicamente las citas sin títulos
    # ni top ten tags
    # Como argumentos tendrá self (por ser un método de una clase) y response (respuesta del servidor).
    # Le agregamos el argumeto **kwargs para desempaquetar el diccionario
    def parse_only_quotes(self, response, **kwargs):
        # Verificamos que hayamos recibido kwargs
        if kwargs:
            # Guardamos en una variable local lo que contenga este diccionario.
            quotes = kwargs['quotes']
            # Se coloca entre corchetes el nombre que definimos en la parte de response.follow() en este caso fue 'quotes'.
        quotes.extend(response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall())
        # Ahora vamos con la tercer página y para esto preguntamos si existe un botón de next.
        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
        else:
            yield {
                'quotes': quotes
            }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_ten_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        # Con la keyword yield convierto mi método en un generador.
        # Y lo que haré será devolver un diccionario para poder hacer mi transformación
        # fácilmente.
        yield {
            'title': title,
            'top_ten_tags': top_ten_tags
        }

        # Para poder cambiar de página dando click en el botón
        # primero asignaremos la ruta XPath a una variable:
        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        # Ahora preguntamos si este botón efectivamente existe (en la última
        # página no existirá)
        if next_page_button_link:
            # El método follow lleva dos parámetros: link a seguir y un callback que nos dice que vamos
            # a hacer con el link que estamos siguiendo.
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
            # Agregamos el argumento cb_kwargs=quotes para pasarlo al metodo que hace referencia el callback.
