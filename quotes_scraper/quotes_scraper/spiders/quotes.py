import scrapy

# Título = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags= //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

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
            'quotes': quotes,
            'top_ten_tags': top_ten_tags
        }
