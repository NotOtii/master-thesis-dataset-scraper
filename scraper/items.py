import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    price_gbp = scrapy.Field()
    in_stock = scrapy.Field()
    rating = scrapy.Field()
    product_page_url = scrapy.Field()
    source_name = scrapy.Field()
    scraped_at = scrapy.Field()
    run_id = scrapy.Field()