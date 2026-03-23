BOT_NAME = "dataset_scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scraper.pipelines.DatasetWriterPipeline": 300,
}

LOG_LEVEL = "INFO"