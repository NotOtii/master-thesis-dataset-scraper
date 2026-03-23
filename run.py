from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scraper.spiders.books_spider import BooksSpider
from scraper import settings as my_settings
from scraper.config_loader import load_config


if __name__ == "__main__":
    config = load_config("config/books_to_scrape.yaml")
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")

    settings_dict = {
        key: value
        for key, value in my_settings.__dict__.items()
        if key.isupper()
    }

    process = CrawlerProcess(settings=settings_dict)
    process.crawl(BooksSpider, config=config, run_id=run_id)
    process.start()