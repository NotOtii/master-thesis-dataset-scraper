import scrapy
from datetime import datetime, timezone

from scraper.items import BookItem


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class BooksSpider(scrapy.Spider):
    name = "books"

    def __init__(self, config=None, run_id="run_001", *args, **kwargs):
        super().__init__(*args, **kwargs)

        if config is None:
            raise ValueError("A config dictionary must be provided to BooksSpider.")

        self.config = config
        self.run_id = run_id
        self.source_name = config["source_name"]
        self.start_urls = config["start_urls"]
        self.allowed_domains = config["allowed_domains"]

    def parse(self, response):
        books = response.css("article.product_pod")

        for book in books:
            item = BookItem()

            title = book.css("h3 a::attr(title)").get()
            raw_price = book.css("p.price_color::text").get()
            raw_rating_class = book.css("p.star-rating::attr(class)").get()
            relative_url = book.css("h3 a::attr(href)").get()

            availability_parts = book.css("p.instock.availability::text").getall()
            availability_text = " ".join(
                x.strip() for x in availability_parts if x.strip()
            )

            rating_word = raw_rating_class.split()[-1] if raw_rating_class else None
            rating_value = RATING_MAP.get(rating_word)

            price_value = None
            if raw_price:
                price_value = float(raw_price.replace("£", "").strip())

            item["title"] = title
            item["price_gbp"] = price_value
            item["in_stock"] = "In stock" in availability_text
            item["rating"] = rating_value
            item["product_page_url"] = response.urljoin(relative_url)
            item["source_name"] = self.source_name
            item["scraped_at"] = datetime.now(timezone.utc).isoformat()
            item["run_id"] = self.run_id

            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)