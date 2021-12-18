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
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
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

        # Mediante esta línea de código vamos de una manera simple traer un número determinado de citas o tags:
        # Generamos una variable donde le preguntamos los siguiente a Scrapy:
        # Si existe dentro de la ejecución de este spider un atributo llamado "top" voy a guardar lo que este dentro
        # de este atributo en la variable 'top', ahora que si este atributo no existe lo que guardaré en mi variable
        # será "None".
        top = getattr(self, 'top', None)
        # Ahora decimos, si existe top haré lo siguiente:
        if top:
            top = int(top)
            # Ahora lo que guardaré en mi variable de top_tags será, mediante slices de python, desde el primer
            # índice hasta "top" que será el valor que nosostros definamos.
            top_tags = top_tags[:top]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
