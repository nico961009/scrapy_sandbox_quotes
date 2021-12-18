import scrapy

# Título = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top tags= //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button=//ul[@class="pager"]//li[@class="next"]/a/@href


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    # Colocamos otras configuraciones para sacar el máximo jugo a este framework
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        # Esta conf nos permitira definir un número entero que le dirá a scrapy el número de peticiones
        # teniendo en cuanta este número definido:
        'CONCURRENT_REQUESTS': 24,
        # Podemos definir la cantidad de memoria RAM que le permitimos usar a Scrapy para trabajar,
        # esto es super útil si tenemos a nuestro scrapper corriendo en la nube para no sobre cargar a nuetro
        # servidor si tenemos muchos  procesos corriendo y no alentar otros servicios que tengamos.
        'MEMUSAGE_LIMIT_MB': 2048,
        # Ahora si se pasa el uso de memoria RAM asignada podemos notificar al administración mediante el siguiente
        # atributo (en este puedo colocar un email para notificar):
        # Al ser una lista puedes asignar más emails.
        'MEMUSAGE_NOTIFY_MAIL': ['beto96_tuzhdez@hotmail.com'],
        # Decirle si va obedecer al archivo robots.txt de la página que estamos scrappeando. Este atributo es recomendable
        # tenerlo siempre activado para evitarnos problemas legales.
        'ROBOTSTXT_OBEY': True,
        # Se puede cambiar el user-agent mediante el siguiente atributo:
        'USER_AGENT': 'Spider_scrapy_curso_PLATZI',
        # Podemos cambiar el encoding del archivo para que no nos de errores en los carácteres, esto lo debemos de hacer
        # mediante el siguiente atributo:
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes.extend(response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall())
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
        top_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
