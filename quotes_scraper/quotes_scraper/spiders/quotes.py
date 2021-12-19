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
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['beto96_tuzhdez@hotmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Spider_scrapy_curso_PLATZI',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']
            quotes_authors = kwargs['quotes_authors']
        quotes.extend(response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall())
        authors.extend(response.xpath(
            '//span/small[@class="author" and @itemprop="author"]/text()').getall())
        quotes_authors.extend(list(zip(quotes, authors)))

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors, 'quotes_authors': quotes_authors})
        else:
            yield {
                'quotes_authors': quotes_authors
            }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        authors = response.xpath(
            '//span/small[@class="author" and @itemprop="author"]/text()').getall()
        top_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        quotes_authors = list(zip(quotes, authors))

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
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors, 'quotes_authors': quotes_authors})
